import math
import six

import torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np


from dlex.models.base import BaseModel
from dlex.utils.logging import logger
from dlex.utils.ops_utils import maybe_cuda


class EncoderRNN(nn.Module):
    def __init__(self, input_size, rnn_type, num_layers, hidden_size, dropout):
        super(EncoderRNN, self).__init__()
        self._hidden_size = hidden_size

        self.rnn = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=rnn_type == "bilstm",
            dropout=dropout
        )

    def forward(self, input_var, input_lengths):
        input_var = nn.utils.rnn.pack_padded_sequence(input_var, input_lengths, batch_first=True)
        output, hidden = self.rnn(input_var)
        output, _ = nn.utils.rnn.pad_packed_sequence(output, batch_first=True)
        return output, input_lengths, hidden


class Attention(BaseModel):
    def __init__(self, params, dataset):
        super().__init__(params, dataset)
        cfg = params.model

        # TODO: note that sos/eos IDs are identical
        self.sos = dataset.sos_token_id
        self.eos = dataset.eos_token_id

        # subsample info
        # +1 means input (+1) and layers outputs (args.elayer)
        subsample = np.ones(cfg.encoder.num_layers + 1, dtype=np.int)
        logger.info('subsample: ' + ' '.join([str(x) for x in subsample]))
        self.subsample = subsample

        # encoder
        self._encoder = self._build_encoder()
        # attention
        self._attention = self._build_attention()
        # decoder
        self._decoder = self._build_decoder()

        # weight initialization
        self.init_like_chainer()

        # options for beam search
        # if 'report_cer' in vars(args) and (args.report_cer or args.report_wer):
        #      recog_args = {'beam_size': cfg.beam_search.beam_size, 'penalty': cfg.beam_search.penalty,
        #                 'ctc_weight': args.ctc_weight, 'maxlenratio': args.maxlenratio,
        #                  'minlenratio': args.minlenratio, 'lm_weight': args.lm_weight,
        #                  'rnnlm': args.rnnlm, 'nbest': args.nbest,
        #                  'space': args.sym_space, 'blank': args.sym_blank}

        #    self.recog_args = argparse.Namespace(**recog_args)
        self.rnnlm = None
        self.logzero = -10000000000.0
        self.criterion = nn.CrossEntropyLoss(ignore_index=-1)

    def _build_encoder(self):
        cfg = self.params.model
        return EncoderRNN(
            input_size=self.dataset.input_size,
            rnn_type=cfg.encoder.rnn_type,
            num_layers=cfg.encoder.num_layers,
            hidden_size=cfg.encoder.hidden_size,
            dropout=cfg.dropout)

    def _build_decoder(self):
        cfg = self.params.model
        return DecoderRNN(
            input_size=cfg.encoder.output_size,
            rnn_type=cfg.decoder.rnn_type,
            num_layers=cfg.decoder.num_layers,
            hidden_size=cfg.decoder.hidden_size,
            output_size=cfg.decoder.output_size,
            vocab_size=self.dataset.output_size,
            attention=self._attention,
            sos_id=self.dataset.sos_token_id,
            eos_id=self.dataset.eos_token_id,
            max_length=cfg.decoder.max_length,
            dropout=cfg.dropout)

    def _build_attention(self):
        cfg = self.params.model
        if cfg.attention.type is None:
            attention = [NoAttention()]
        elif cfg.attention.type == 'bahdanau':
            self._test = BahdanauAttention(
                encoder_output_size=cfg.encoder.output_size,
                decoder_hidden_size=cfg.decoder.hidden_size,
                attention_dim=cfg.attention.size,
            )
            attention = [self._test]
        return attention

    def init_like_chainer(self):
        """Initialize weight like chainer

        chainer basically uses LeCun way: W ~ Normal(0, fan_in ** -0.5), b = 0
        pytorch basically uses W, b ~ Uniform(-fan_in**-0.5, fan_in**-0.5)

        however, there are two exceptions as far as I know.
        - EmbedID.W ~ Normal(0, 1)
        - LSTM.upward.b[forget_gate_range] = 1 (but not used in NStepLSTM)
        """

        def lecun_normal_init_parameters(module):
            for p in module.parameters():
                data = p.data
                if data.dim() == 1:
                    # bias
                    data.zero_()
                elif data.dim() == 2:
                    # linear weight
                    n = data.size(1)
                    stdv = 1. / math.sqrt(n)
                    data.normal_(0, stdv)
                elif data.dim() == 4:
                    # conv weight
                    n = data.size(1)
                    for k in data.size()[2:]:
                        n *= k
                    stdv = 1. / math.sqrt(n)
                    data.normal_(0, stdv)
                else:
                    raise NotImplementedError

        def set_forget_bias_to_one(bias):
            n = bias.size(0)
            start, end = n // 4, n // 2
            bias.data[start:end].fill_(1.)

        lecun_normal_init_parameters(self)
        # exceptions
        # embed weight ~ Normal(0, 1)
        self._decoder.embed.weight.data.normal_(0, 1)
        # forget-bias = 1.0
        # https://discuss.pytorch.org/t/set-forget-gate-bias-of-lstm/1745
        for l in six.moves.range(len(self._decoder.decoder)):
            set_forget_bias_to_one(self._decoder.decoder[l].bias_ih)

    def forward(self, batch):
        """E2E forward

        :param torch.Tensor xs_pad: batch of padded input sequences (B, Tmax, idim)
        :param torch.Tensor ilens: batch of lengths of input sequences (B)
        :param torch.Tensor ys_pad: batch of padded character id sequence tensor (B, Lmax)
        :return: ctc loass value
        :rtype: torch.Tensor
        :return: attention loss value
        :rtype: torch.Tensor
        :return: accuracy in attention decoder
        :rtype: float
        """
        encoder_outputs, encoder_output_lens, encoder_hiddens = self._encoder(batch['X'], batch['X_len'])
        return self._decoder(encoder_outputs, encoder_output_lens, batch['Y'])

    def get_loss(self, batch, output):
        y = batch['Y'][:, 1:]
        batch_size = y.shape[0]
        max_length = y.shape[1]
        decoder_outputs, _, _ = output
        decoder_outputs = decoder_outputs.view(batch_size, -1, self.dataset.output_size)
        loss = sum([
            self.criterion(decoder_outputs[:, i, :], y[:, i])
            for i in range(max_length)
            ])
        loss /= max_length
        # -1: eos, which is removed in the loss computation
        # loss *= (np.mean(batch['Y_len']) - 1)
        return loss

    def infer(self, batch):
        if self.params.model.decoding_method == 'greedy':
            encoder_outputs, encoder_output_lens, encoder_hiddens = self._encoder(batch['X'], batch['X_len'])
            decoder_outputs, sequences, sequence_lens = self._decoder(
                encoder_outputs=encoder_outputs,
                encoder_output_lens=encoder_output_lens,
                decoder_inputs=None,
                use_teacher_forcing=False)
            return sequences, batch['Y_len']
        elif self.params.model.decoding_method == 'beam_search':
            encoder_outputs, encoder_output_lens, encoder_hiddens = self._encoder(batch['X'], batch['X_len'])
            decoder_outputs, sequences, sequence_lens = self._decoder.recognize_beam_batch(
                encoder_outputs=encoder_outputs,
                encoder_output_lens=encoder_output_lens,
                decoder_inputs=None,
                use_teacher_forcing=False)
            return sequences, batch['Y_len']

            nbest_hypotheses = self._decoder.recognize_beam_batch(
                encoder_outputs,
                encoder_output_lens,
                lpz,
                self.recog_args, self.char_list,
                self.rnnlm)

        # Note(kamo): In order to work with DataParallel, on pytorch==0.4,
        # the return value must be torch.CudaTensor, or tuple/list/dict of it.
        # Neither CPUTensor nor float/int value can be used
        # because NCCL communicates between GPU devices.
        # device = next(self.parameters()).device

    def recognize(self, x, recog_args, char_list, rnnlm=None):
        """E2E beam search

        :param ndarray x: input acoustic feature (T, D)
        :param Namespace recog_args: argument Namespace containing options
        :param list char_list: list of characters
        :param torch.nn.Module rnnlm: language model module
        :return: N-best decoding results
        :rtype: list
        """
        prev = self.training
        self.eval()
        # subsample frame
        h, ilen = self.subsample_frames(x)

        # 1. encoder
        # make a utt list (1) to use the same interface for encoder
        h, _, _ = self.enc(h.unsqueeze(0), ilen)

        # calculate log P(z_t|X) for CTC scores
        if recog_args.ctc_weight > 0.0:
            lpz = self.ctc.log_softmax(h)[0]
        else:
            lpz = None

        # 2. decoder
        # decode the first utterance
        y = self.dec.recognize_beam(h[0], lpz, recog_args, char_list, rnnlm)

        if prev:
            self.train()
        return y

    def recognize_batch(self, xs, recog_args, char_list, rnnlm=None):
        """E2E beam search

        :param list xs: list of input acoustic feature arrays [(T_1, D), (T_2, D), ...]
        :param Namespace recog_args: argument Namespace containing options
        :param list char_list: list of characters
        :param torch.nn.Module rnnlm: language model module
        :return: N-best decoding results
        :rtype: list
        """
        prev = self.training
        self.eval()
        # subsample frame
        xs = [xx[::self.subsample[0], :] for xx in xs]
        ilens = np.fromiter((xx.shape[0] for xx in xs), dtype=np.int64)
        hs = [to_device(self, torch.from_numpy(np.array(xx, dtype=np.float32)))
              for xx in xs]

        # 1. encoder
        xpad = pad_list(hs, 0.0)
        hpad, hlens, _ = self.enc(xpad, ilens)

        # calculate log P(z_t|X) for CTC scores
        if recog_args.ctc_weight > 0.0:
            lpz = self.ctc.log_softmax(hpad)
        else:
            lpz = None

        # 2. decoder
        hlens = torch.tensor(list(map(int, hlens)))  # make sure hlens is tensor
        y = self.dec.recognize_beam_batch(hpad, hlens, lpz, recog_args, char_list, rnnlm)

        if prev:
            self.train()
        return y

    def calculate_all_attentions(self, batch):
        with torch.no_grad():
            encoder_outputs, encoder_output_lens, _ = self._encoder(batch['X'], batch['X_len'])
            return self._decoder.calculate_all_attentions(encoder_outputs, encoder_output_lens, batch['Y'])

    def subsample_frames(self, x):
        # subsample frame
        x = x[::self.subsample[0], :]
        ilen = [x.shape[0]]
        h = to_device(self, torch.from_numpy(
            np.array(x, dtype=np.float32)))
        h.contiguous()
        return h, ilen


class NMT(Attention):
    def __init__(self, params, dataset):
        super().__init__(params, dataset)

    def _build_encoder(self):
        cfg = self.params.model

        self.embedding = nn.Embedding(
            num_embeddings=self.dataset.input_size,
            embedding_dim=cfg.encoder.input_size)
        if cfg.embedding is not None:
            # TODO: implement custom embedding
            pass
        self.embedding.requires_grad = cfg.update_embedding

        return EncoderRNN(
            input_size=cfg.encoder.input_size,
            rnn_type=cfg.encoder.rnn_type,
            num_layers=cfg.encoder.num_layers,
            hidden_size=cfg.encoder.hidden_size,
            dropout=cfg.dropout
        )

    def forward(self, batch):
        return super().forward(dict(
            X=self.embedding(batch['X']),
            X_len=batch['X_len'],
            Y=batch['Y'],
            Y_len=batch['Y_len']
        ))

    def infer(self, batch):
        return super().infer(dict(
            X=self.embedding(batch['X']),
            X_len=batch['X_len'],
            Y=batch['Y'],
            Y_len=batch['Y_len']
        ))


class TeacherForcingDecoder(nn.Module):
    def __init__(self, eos_token_id):
        self.eos_token_id = eos_token_id
        super().__init__()

    def forward(self, encoder_outputs, decoder_inputs, decoder_outputs):
        batch_size = encoder_outputs.size(0)
        max_length = decoder_outputs.size(1)
        sequence_symbols = []
        lengths = np.array([max_length] * batch_size)
        for step in range(decoder_outputs.size(1)):
            symbols = decoder_outputs[:, step, :].topk(1)[1]
            sequence_symbols.append(symbols)
            eos_batches = decoder_inputs[:, step].eq(self.eos_token_id)
            if eos_batches.dim() > 0:
                eos_batches = eos_batches.cpu().view(-1).numpy()
                update_idx = ((lengths > step) & eos_batches) != 0
                lengths[update_idx] = step
        decoder_outputs = decoder_outputs.permute(1, 0, 2)
        #print("basic")
        #for i in range(batch_size):
        #    for j in range(max_length):
        #        print(sequence_symbols[j][i].item(), end=' ')
        #    print()
        return sequence_symbols, lengths, decoder_outputs


class DecoderRNN(nn.Module):
    """Decoder module

    :param int eprojs: # encoder projection units
    :param int odim: dimension of outputs
    :param str dtype: gru or lstm
    :param int dlayers: # decoder layers
    :param int dunits: # decoder units
    :param int sos: start of sequence symbol id
    :param int eos: end of sequence symbol id
    :param torch.nn.Module att: attention module
    :param int verbose: verbose level
    :param list char_list: list of character strings
    :param ndarray labeldist: distribution of label smoothing
    :param float lsm_weight: label smoothing weight
    :param float sampling_probability: scheduled sampling probability
    :param float dropout: dropout rate
    """

    def __init__(self, input_size, rnn_type, num_layers, hidden_size, output_size, vocab_size, attention, sos_id, eos_id, max_length, dropout):
        super().__init__()
        self.embed = torch.nn.Embedding(vocab_size, input_size)
        self.dropout_emb = torch.nn.Dropout(p=dropout)

        self.decoder = torch.nn.ModuleList()
        self.dropout_dec = torch.nn.ModuleList()
        self.decoder += [
            torch.nn.LSTMCell(hidden_size + input_size, hidden_size) if rnn_type == "lstm"
            else torch.nn.GRUCell(hidden_size + input_size, hidden_size)]
        self.dropout_dec += [torch.nn.Dropout(p=dropout)]
        for _ in six.moves.range(1, num_layers):
            self.decoder += [
                torch.nn.LSTMCell(hidden_size, hidden_size) if rnn_type == "lstm"
                else torch.nn.GRUCell(hidden_size + input_size, hidden_size)]
            self.dropout_dec += [torch.nn.Dropout(p=dropout)]
            # NOTE: dropout is applied only for the vertical connections
            # see https://arxiv.org/pdf/1409.2329.pdf
        self.ignore_id = -1
        self.output = torch.nn.Linear(hidden_size, vocab_size)

        self.loss = None
        self._attention = attention
        self._sos_id = sos_id
        self._eos_id = eos_id
        # self.char_list = char_list
        # for label smoothing
        # self.labeldist = labeldist
        # self.vlabeldist = None
        # self.lsm_weight = lsm_weight
        self._max_length = max_length
        self._dropout = dropout
        self._num_layers = num_layers
        self._hidden_size = hidden_size
        self._rnn_type = rnn_type

        self._logzero = -10000000000.0

    def zero_state(self, hs_pad):
        return hs_pad.new_zeros(hs_pad.size(0), self._hidden_size)

    def rnn_forward(self, ey, z_list, c_list, z_prev, c_prev):
        if self._rnn_type == "lstm":
            z_list[0], c_list[0] = self.decoder[0](ey, (z_prev[0], c_prev[0]))
            for l in six.moves.range(1, self._num_layers):
                z_list[l], c_list[l] = self.decoder[l](
                    self.dropout_dec[l - 1](z_list[l - 1]), (z_prev[l], c_prev[l]))
        else:
            z_list[0] = self.decoder[0](ey, z_prev[0])
            for l in six.moves.range(1, self._num_layers):
                z_list[l] = self.decoder[l](self.dropout_dec[l - 1](z_list[l - 1]), z_prev[l])
        return z_list, c_list

    def forward(self, encoder_outputs, encoder_output_lens, decoder_inputs, strm_idx=0, use_teacher_forcing=True):
        """Decoder forward

        :param torch.Tensor hs_pad: batch of padded hidden state sequences (B, Tmax, D)
        :param torch.Tensor hlens: batch of lengths of hidden state sequences (B)
        :param torch.Tensor ys_pad: batch of padded character id sequence tensor (B, Lmax)
        :param int strm_idx: stream index indicates the index of decoding stream.
        :return: attention loss value
        :rtype: torch.Tensor
        :return: accuracy
        :rtype: float
        """
        # TODO(kan-bayashi): need to make more smart way
        batch_size = encoder_outputs.size(0)
        max_length = decoder_inputs.size(1) if decoder_inputs is not None else self._max_length
        # ys = [y[y != self.ignore_id] for y in decoder_inputs]  # parse padded ys
        # attention index for the attention module
        # in SPA (speaker parallel attention), att_idx is used to select attention module. In other cases, it is 0.
        att_idx = min(strm_idx, len(self._attention) - 1)

        # initialization
        c_list = [self.zero_state(encoder_outputs)]
        z_list = [self.zero_state(encoder_outputs)]
        for _ in six.moves.range(1, self._num_layers):
            c_list.append(self.zero_state(encoder_outputs))
            z_list.append(self.zero_state(encoder_outputs))
        att_w = None
        z_all = []
        self._attention[att_idx].reset()  # reset pre-computation of h

        if use_teacher_forcing:
            decoder_embedded_inputs = self.dropout_emb(self.embed(decoder_inputs[:, :-1]))  # utt x olen x zdim

            # loop for an output sequence
            for i in six.moves.range(decoder_inputs.size(1) - 1):
                att_c, att_w = self._attention[att_idx](encoder_outputs, encoder_output_lens, self.dropout_dec[0](z_list[0]), att_w)
                ey = torch.cat((decoder_embedded_inputs[:, i, :], att_c), dim=1)  # utt x (zdim + hdim)
                z_list, c_list = self.rnn_forward(ey, z_list, c_list, z_list, c_list)
                z_all.append(self.dropout_dec[-1](z_list[-1]))
        else:
            for step in six.moves.range(max_length):
                att_c, att_w = self._attention[att_idx](encoder_outputs, encoder_output_lens,
                                                        self.dropout_dec[0](z_list[0]), att_w)
                if step == 0:
                    embedded_sos = self.dropout_emb(self.embed(
                        maybe_cuda(torch.full((batch_size, ), self._sos_id, dtype=torch.int64))))
                    ey = torch.cat((embedded_sos, att_c), dim=1)
                else:
                    z_out = self.output(z_all[-1])
                    _, z_out = torch.max(z_out.detach(), dim=1)
                    z_out = self.dropout_emb(self.embed(z_out.cuda()))
                    ey = torch.cat((z_out, att_c), dim=1)  # utt x (zdim + hdim)

                z_list, c_list = self.rnn_forward(ey, z_list, c_list, z_list, c_list)
                z_all.append(self.dropout_dec[-1](z_list[-1]))

        z_all = torch.stack(z_all, dim=1).view(batch_size, -1, self._hidden_size)
        y_all = self.output(z_all)
        _, sequences = y_all.max(-1)

        lengths = np.array([max_length] * batch_size)
        for step in six.moves.range(max_length - 1):
            eos_batches = sequences[:, step].eq(self._eos_id)
            if eos_batches.dim() > 0:
                eos_batches = eos_batches.cpu().view(-1).numpy()
                update_idx = ((lengths > step) & eos_batches) != 0
                lengths[update_idx] = step

        # acc = th_accuracy(y_all, ys_out_pad, ignore_label=self.ignore_id)
        # logger.info('att loss:' + ''.join(str(self.loss.item()).split('\n')))

        return y_all, sequences, lengths

    def recognize_beam(self, encoder_outputs, recog_args, char_list, rnn_language_model=None, strm_idx=0):
        """beam search implementation

        :param torch.Tensor h: encoder hidden state (T, eprojs)
        :param Namespace recog_args: argument Namespace containing options
        :param char_list: list of character strings
        :param torch.nn.Module rnn_language_model: language module
        :param int strm_idx: stream index for speaker parallel attention in multi-speaker case
        :return: N-best decoding results
        :rtype: list of dicts
        """
        logger.info('input lengths: ' + str(encoder_outputs.size(0)))
        att_idx = min(strm_idx, len(self.att) - 1)
        # initialization
        c_list = [self.zero_state(encoder_outputs.unsqueeze(0))]
        z_list = [self.zero_state(encoder_outputs.unsqueeze(0))]
        for _ in six.moves.range(1, self._num_layers):
            c_list.append(self.zero_state(encoder_outputs.unsqueeze(0)))
            z_list.append(self.zero_state(encoder_outputs.unsqueeze(0)))
        a = None
        self.att[att_idx].reset()  # reset pre-computation of h

        # search parms
        beam = recog_args.beam_size
        penalty = recog_args.penalty

        # preprate sos
        y = self.sos
        vy = h.new_zeros(1).long()

        if recog_args.maxlenratio == 0:
            maxlen = h.shape[0]
        else:
            # maxlen >= 1
            maxlen = max(1, int(recog_args.maxlenratio * h.size(0)))
        minlen = int(recog_args.minlenratio * h.size(0))
        logger.info('max output length: ' + str(maxlen))
        logger.info('min output length: ' + str(minlen))

        # initialize hypothesis
        if rnn_language_model:
            hyp = {'score': 0.0, 'yseq': [y], 'c_prev': c_list,
                   'z_prev': z_list, 'a_prev': a, 'rnn_language_model_prev': None}
        else:
            hyp = {'score': 0.0, 'yseq': [y], 'c_prev': c_list, 'z_prev': z_list, 'a_prev': a}
        hypotheses = [hyp]
        ended_hypotheses = []

        for i in six.moves.range(maxlen):
            logger.debug('position ' + str(i))

            hypotheses_best_kept = []
            for hyp in hypotheses:
                vy.unsqueeze(1)
                vy[0] = hyp['yseq'][i]
                ey = self.dropout_emb(self.embed(vy))  # utt list (1) x zdim
                ey.unsqueeze(0)
                att_c, att_w = self.att[att_idx](h.unsqueeze(0), [encoder_outputs.size(0)],
                                                 self.dropout_dec[0](hyp['z_prev'][0]), hyp['a_prev'])
                ey = torch.cat((ey, att_c), dim=1)  # utt(1) x (zdim + hdim)
                z_list, c_list = self.rnn_forward(ey, z_list, c_list, hyp['z_prev'], hyp['c_prev'])

                # get n-best local scores and their ids
                local_att_scores = F.log_softmax(self.output(self.dropout_dec[-1](z_list[-1])), dim=1)
                if rnn_language_model:
                    rnn_language_model_state, local_lm_scores = rnn_language_model.predict(hyp['rnn_language_model_prev'], vy)
                    local_scores = local_att_scores + recog_args.lm_weight * local_lm_scores
                else:
                    local_scores = local_att_scores

                local_best_scores, local_best_ids = torch.topk(local_scores, beam, dim=1)

                for j in six.moves.range(beam):
                    new_hyp = {}
                    # [:] is needed!
                    new_hyp['z_prev'] = z_list[:]
                    new_hyp['c_prev'] = c_list[:]
                    new_hyp['a_prev'] = att_w[:]
                    new_hyp['score'] = hyp['score'] + local_best_scores[0, j]
                    new_hyp['yseq'] = [0] * (1 + len(hyp['yseq']))
                    new_hyp['yseq'][:len(hyp['yseq'])] = hyp['yseq']
                    new_hyp['yseq'][len(hyp['yseq'])] = int(local_best_ids[0, j])
                    if rnn_language_model:
                        new_hyp['rnn_language_model_prev'] = rnn_language_model_state
                    # will be (2 x beam) hypotheses at most
                    hypotheses_best_kept.append(new_hyp)

                hypotheses_best_kept = sorted(
                    hypotheses_best_kept, key=lambda x: x['score'], reverse=True)[:beam]

            # sort and get nbest
            hypotheses = hypotheses_best_kept
            logger.debug('number of pruned hypotheses: ' + str(len(hypotheses)))
            logger.debug(
                'best hypo: ' + ''.join([char_list[int(x)] for x in hypotheses[0]['yseq'][1:]]))

            # add eos in the final loop to avoid that there are no ended hypotheses
            if i == maxlen - 1:
                logger.info('adding <eos> in the last position in the loop')
                for hyp in hypotheses:
                    hyp['yseq'].append(self.eos)

            # add ended hypotheses to a final list, and removed them from current hypotheses
            # (this will be a problem, number of hypotheses < beam)
            remained_hypotheses = []
            for hyp in hypotheses:
                if hyp['yseq'][-1] == self.eos:
                    # only store the sequence that has more than minlen outputs
                    # also add penalty
                    if len(hyp['yseq']) > minlen:
                        hyp['score'] += (i + 1) * penalty
                        if rnn_language_model:  # Word LM needs to add final <eos> score
                            hyp['score'] += recog_args.lm_weight * rnn_language_model.final(
                                hyp['rnn_language_model_prev'])
                        ended_hypotheses.append(hyp)
                else:
                    remained_hypotheses.append(hyp)

            # end detection
            if end_detect(ended_hypotheses, i) and recog_args.maxlenratio == 0.0:
                logger.info('end detected at %d', i)
                break

            hypotheses = remained_hypotheses
            if len(hypotheses) > 0:
                logger.debug('remaining hypotheses: ' + str(len(hypotheses)))
            else:
                logger.info('no hypothesis. Finish decoding.')
                break

            for hyp in hypotheses:
                logger.debug(
                    'hypo: ' + ''.join([char_list[int(x)] for x in hyp['yseq'][1:]]))

            logger.debug('number of ended hypotheses: ' + str(len(ended_hypotheses)))

        nbest_hypotheses = sorted(
            ended_hypotheses, key=lambda x: x['score'], reverse=True)[:min(len(ended_hypotheses), recog_args.nbest)]

        # check number of hypotheses
        if len(nbest_hypotheses) == 0:
            logger.warning('there is no N-best results, perform recognition again with smaller minlenratio.')
            # should copy because Namespace will be overwritten globally
            recog_args = Namespace(**vars(recog_args))
            recog_args.minlenratio = max(0.0, recog_args.minlenratio - 0.1)
            return self.recognize_beam(h, lpz, recog_args, char_list, rnn_language_model)

        logger.info('total log probability: ' + str(nbest_hypotheses[0]['score']))
        logger.info('normalized log probability: ' + str(nbest_hypotheses[0]['score'] / len(nbest_hypotheses[0]['yseq'])))

        # remove sos
        return nbest_hypotheses

    def recognize_beam_batch(self, encoder_outputs, encoder_output_lens, recog_args, char_list, rnn_language_model=None,
                             normalize_score=True, strm_idx=0):
        logger.info('input lengths: ' + str(encoder_outputs.size(1)))
        att_idx = min(strm_idx, len(self.att) - 1)
        encoder_outputs = mask_by_length(encoder_outputs, encoder_output_lens, 0.0)

        # search params
        batch = len(encoder_output_lens)
        beam = recog_args.beam_size
        penalty = recog_args.penalty

        n_bb = batch * beam
        n_bo = beam * self.odim
        n_bbo = n_bb * self.odim
        pad_b = maybe_cuda(torch.LongTensor([i * beam for i in six.moves.range(batch)]).view(-1, 1))
        pad_bo = maybe_cuda(torch.LongTensor([i * n_bo for i in six.moves.range(batch)]).view(-1, 1))
        pad_o = maybe_cuda(torch.LongTensor([i * self.odim for i in six.moves.range(n_bb)]).view(-1, 1))

        max_encoder_output_len = int(max(encoder_output_lens))
        if recog_args.maxlenratio == 0:
            max_len = max_encoder_output_len
        else:
            max_len = max(1, int(recog_args.maxlenratio * max_encoder_output_len))
        min_len = int(recog_args.minlenratio * max_encoder_output_len)

        # initialization
        c_prev = [maybe_cuda(torch.zeros(n_bb, self.dunits)) for _ in range(self.dlayers)]
        z_prev = [maybe_cuda(torch.zeros(n_bb, self.dunits)) for _ in range(self.dlayers)]
        c_list = [maybe_cuda(torch.zeros(n_bb, self.dunits)) for _ in range(self.dlayers)]
        z_list = [maybe_cuda(torch.zeros(n_bb, self.dunits)) for _ in range(self.dlayers)]
        vscores = maybe_cuda(torch.zeros(batch, beam))

        a_prev = None
        rnn_language_model_prev = None

        self.att[att_idx].reset()  # reset pre-computation of h

        yseq = [[self.sos] for _ in six.moves.range(n_bb)]
        accum_odim_ids = [self.sos for _ in six.moves.range(n_bb)]
        stop_search = [False for _ in six.moves.range(batch)]
        nbest_hypotheses = [[] for _ in six.moves.range(batch)]
        ended_hypotheses = [[] for _ in range(batch)]

        exp_encoder_output_lens = encoder_output_lens.repeat(beam).view(beam, batch).transpose(0, 1).contiguous()
        exp_encoder_output_lens = exp_encoder_output_lens.view(-1).tolist()
        exp_h = encoder_outputs.unsqueeze(1).repeat(1, beam, 1, 1).contiguous()
        exp_h = exp_h.view(n_bb, encoder_outputs.size()[1], encoder_outputs.size()[2])

        for i in six.moves.range(max_len):
            logger.debug('position ' + str(i))

            vy = maybe_cuda(torch.LongTensor(get_last_yseq(yseq)))
            ey = self.dropout_emb(self.embed(vy))
            att_c, att_w = self.att[att_idx](exp_h, exp_encoder_output_lens, self.dropout_dec[0](z_prev[0]), a_prev)
            ey = torch.cat((ey, att_c), dim=1)

            # attention decoder
            z_list, c_list = self.rnn_forward(ey, z_list, c_list, z_prev, c_prev)
            local_scores = F.log_softmax(self.output(self.dropout_dec[-1](z_list[-1])), dim=1)

            # rnn_language_model
            if rnn_language_model:
                rnn_language_model_state, local_lm_scores = rnn_language_model.buff_predict(rnn_language_model_prev, vy, n_bb)
                local_scores = local_scores + recog_args.lm_weight * local_lm_scores
            local_scores = local_scores.view(batch, n_bo)
            local_scores = local_scores.view(batch, beam, self.odim)

            if i == 0:
                local_scores[:, 1:, :] = self.logzero
            local_best_scores, local_best_odims = torch.topk(local_scores.view(batch, beam, self.odim),
                                                             beam, 2)
            # local pruning (via xp)
            local_scores = np.full((n_bbo,), self.logzero)
            _best_odims = local_best_odims.view(n_bb, beam) + pad_o
            _best_odims = _best_odims.view(-1).cpu().numpy()
            _best_score = local_best_scores.view(-1).cpu().detach().numpy()
            local_scores[_best_odims] = _best_score
            local_scores = maybe_cuda(torch.from_numpy(local_scores).float()).view(batch, beam, self.odim)

            # (or indexing)
            # local_scores = to_cuda(self, torch.full((batch, beam, self.odim), self.logzero))
            # _best_odims = local_best_odims
            # _best_score = local_best_scores
            # for si in six.moves.range(batch):
            # for bj in six.moves.range(beam):
            # for bk in six.moves.range(beam):
            # local_scores[si, bj, _best_odims[si, bj, bk]] = _best_score[si, bj, bk]

            eos_vscores = local_scores[:, :, self.eos] + vscores
            vscores = vscores.view(batch, beam, 1).repeat(1, 1, self.odim)
            vscores[:, :, self.eos] = self.logzero
            vscores = (vscores + local_scores).view(batch, n_bo)

            # global pruning
            accum_best_scores, accum_best_ids = torch.topk(vscores, beam, 1)
            accum_odim_ids = torch.fmod(accum_best_ids, self.odim).view(-1).data.cpu().tolist()
            accum_padded_odim_ids = (torch.fmod(accum_best_ids, n_bo) + pad_bo).view(-1).data.cpu().tolist()
            accum_padded_beam_ids = (torch.div(accum_best_ids, self.odim) + pad_b).view(-1).data.cpu().tolist()

            y_prev = yseq[:][:]
            yseq = index_select_list(yseq, accum_padded_beam_ids)
            yseq = append_ids(yseq, accum_odim_ids)
            vscores = accum_best_scores
            vidx = maybe_cuda(torch.LongTensor(accum_padded_beam_ids))

            if isinstance(att_w, torch.Tensor):
                a_prev = torch.index_select(att_w.view(n_bb, *att_w.shape[1:]), 0, vidx)
            elif isinstance(att_w, list):
                # handle the case of multi-head attention
                a_prev = [torch.index_select(att_w_one.view(n_bb, -1), 0, vidx) for att_w_one in att_w]
            else:
                # handle the case of location_recurrent when return is a tuple
                a_prev_ = torch.index_select(att_w[0].view(n_bb, -1), 0, vidx)
                h_prev_ = torch.index_select(att_w[1][0].view(n_bb, -1), 0, vidx)
                c_prev_ = torch.index_select(att_w[1][1].view(n_bb, -1), 0, vidx)
                a_prev = (a_prev_, (h_prev_, c_prev_))
            z_prev = [torch.index_select(z_list[li].view(n_bb, -1), 0, vidx) for li in range(self.dlayers)]
            c_prev = [torch.index_select(c_list[li].view(n_bb, -1), 0, vidx) for li in range(self.dlayers)]

            if rnn_language_model:
                rnn_language_model_prev = index_select_lm_state(rnn_language_model_state, 0, vidx)

            # pick ended hypotheses
            if i > min_len:
                k = 0
                penalty_i = (i + 1) * penalty
                thr = accum_best_scores[:, -1]
                for samp_i in six.moves.range(batch):
                    if stop_search[samp_i]:
                        k = k + beam
                        continue
                    for beam_j in six.moves.range(beam):
                        if eos_vscores[samp_i, beam_j] > thr[samp_i]:
                            yk = y_prev[k][:]
                            yk.append(self.eos)
                            if len(yk) < encoder_output_lens[samp_i]:
                                _vscore = eos_vscores[samp_i][beam_j] + penalty_i
                                if normalize_score:
                                    _vscore = _vscore / len(yk)
                                _score = _vscore.data.cpu().numpy()
                                ended_hypotheses[samp_i].append({'yseq': yk, 'vscore': _vscore, 'score': _score})
                        k = k + 1

            # end detection
            stop_search = [stop_search[samp_i] or end_detect(ended_hypotheses[samp_i], i)
                           for samp_i in six.moves.range(batch)]
            stop_search_summary = list(set(stop_search))
            if len(stop_search_summary) == 1 and stop_search_summary[0]:
                break

            torch.cuda.empty_cache()

        dummy_hypotheses = [{'yseq': [self.sos, self.eos], 'score': np.array([-float('inf')])}]
        ended_hypotheses = [ended_hypotheses[samp_i] if len(ended_hypotheses[samp_i]) != 0 else dummy_hypotheses
                      for samp_i in six.moves.range(batch)]
        n_best_hypotheses = [sorted(ended_hypotheses[samp_i], key=lambda x: x['score'],
                             reverse=True)[:min(len(ended_hypotheses[samp_i]), recog_args.n_best)]
                      for samp_i in six.moves.range(batch)]

        return n_best_hypotheses

    def calculate_all_attentions(self, encoder_outputs, encoder_output_lens, decoder_inputs, strm_idx=0):
        """Calculate all of attentions

        :param torch.Tensor hs_pad: batch of padded hidden state sequences (B, Tmax, D)
        :param torch.Tensor hlen: batch of lengths of hidden state sequences (B)
        :param torch.Tensor ys_pad: batch of padded character id sequence tensor (B, Lmax)
        :param int strm_idx: stream index for parallel speaker attention in multi-speaker case
        :return: attention weights with the following shape,
            1) multi-head case => attention weights (B, H, Lmax, Tmax),
            2) other case => attention weights (B, Lmax, Tmax).
        :rtype: float ndarray
        """
        # TODO(kan-bayashi): need to make more smart way
        ys = [y[y != self.ignore_id] for y in decoder_inputs]  # parse padded ys
        att_idx = min(strm_idx, len(self.att) - 1)

        # hlen should be list of integer
        hlen = list(map(int, encoder_output_lens))

        ys_in_pad = decoder_inputs[:, :-1]
        ys_out_pad = decoder_inputs[:, 1:]

        # get length info
        max_length = ys_out_pad.size(1)

        # initialization
        c_list = [self.zero_state(encoder_outputs)]
        z_list = [self.zero_state(encoder_outputs)]
        for _ in six.moves.range(1, self.dlayers):
            c_list.append(self.zero_state(encoder_outputs))
            z_list.append(self.zero_state(encoder_outputs))
        att_w = None
        att_ws = []
        self.att[att_idx].reset()  # reset pre-computation of h

        # pre-computation of embedding
        eys = self.dropout_emb(self.embed(ys_in_pad))  # utt x olen x zdim

        # loop for an output sequence
        for i in six.moves.range(max_length):
            att_c, att_w = self.att[att_idx](encoder_outputs, hlen, self.dropout_dec[0](z_list[0]), att_w)
            ey = torch.cat((eys[:, i, :], att_c), dim=1)  # utt x (zdim + hdim)
            z_list, c_list = self.rnn_forward(ey, z_list, c_list, z_list, c_list)
            att_ws.append(att_w)

        # convert to numpy array with the shape (B, Lmax, Tmax)
        att_ws = att_to_numpy(att_ws, self._attention[att_idx])
        return att_ws


def make_pad_mask(lengths):
    """Function to make mask tensor containing indices of padded part

    e.g.: lengths = [5, 3, 2]
          mask = [[0, 0, 0, 0 ,0],
                  [0, 0, 0, 1, 1],
                  [0, 0, 1, 1, 1]]

    :param list lengths: list of lengths (B)
    :return: mask tensor containing indices of padded part (B, Tmax)
    :rtype: torch.Tensor
    """
    if not isinstance(lengths, list):
        lengths = lengths.tolist()
    bs = int(len(lengths))
    maxlen = int(max(lengths))
    seq_range = torch.arange(0, maxlen, dtype=torch.int64)
    seq_range_expand = seq_range.unsqueeze(0).expand(bs, maxlen)
    seq_length_expand = seq_range_expand.new(lengths).unsqueeze(-1)
    return maybe_cuda(seq_range_expand >= seq_length_expand)


class NoAttention(torch.nn.Module):
    def __init__(self):
        super(NoAttention, self).__init__()
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.c = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.c = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev):
        """NoAttention forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B, T_max, D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: dummy (does not use)
        :param torch.Tensor att_prev: dummy (does not use)
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights
        :rtype: torch.Tensor
        """
        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)

        # initialize attention weight with uniform dist.
        if att_prev is None:
            # if no bias, 0 0-pad goes 0
            mask = 1. - make_pad_mask(enc_hs_len).float()
            att_prev = mask / mask.new(enc_hs_len.float()).unsqueeze(-1)
            att_prev = att_prev.to(self.enc_h)
            self.c = torch.sum(self.enc_h * att_prev.view(batch, self.h_length, 1), dim=1)

        return self.c, att_prev


class AttDot(torch.nn.Module):
    """Dot product attention

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    """

    def __init__(self, eprojs, dunits, att_dim):
        super(AttDot, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, scaling=2.0):
        """AttDot forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: dummy (does not use)
        :param torch.Tensor att_prev: dummy (does not use)
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weight (B x T_max)
        :rtype: torch.Tensor
        """

        batch = enc_hs_pad.size(0)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = torch.tanh(self.mlp_enc(self.enc_h))

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        e = torch.sum(self.pre_compute_enc_h * torch.tanh(self.mlp_dec(dec_z)).view(batch, 1, self.att_dim),
                      dim=2)  # utt x frame

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = maybe_cuda(make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)
        return c, w


class BahdanauAttention(nn.Module):
    """Additive attention

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    """

    def __init__(self, encoder_output_size, decoder_hidden_size, attention_dim):
        super().__init__()
        self.mlp_enc = torch.nn.Linear(encoder_output_size, attention_dim)
        self.mlp_dec = torch.nn.Linear(decoder_hidden_size, attention_dim, bias=False)
        self.gvec = torch.nn.Linear(attention_dim, 1)
        self._decoder_hidden_size = decoder_hidden_size
        self._encoder_output_size = encoder_output_size
        self._attention_dim = attention_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, encoder_outputs, encoder_output_lens, decoder_hidden_state, att_prev, scaling=2.0):
        """AttLoc forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: dummy (does not use)
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights (B x T_max)
        :rtype: torch.Tensor
        """

        batch = len(encoder_outputs)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = encoder_outputs  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if decoder_hidden_state is None:
            decoder_hidden_state = encoder_outputs.new_zeros(batch, self._decoder_hidden_size)
        else:
            decoder_hidden_state = decoder_hidden_state.view(batch, self._decoder_hidden_size)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(decoder_hidden_state).view(batch, 1, self._attention_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = maybe_cuda(make_pad_mask(encoder_output_lens))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        return c, w


class AttLoc(torch.nn.Module):
    """location-aware attention

    Reference: Attention-Based Models for Speech Recognition
        (https://arxiv.org/pdf/1506.07503.pdf)

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, att_dim, aconv_chans, aconv_filts):
        super(AttLoc, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.mlp_att = torch.nn.Linear(aconv_chans, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, scaling=2.0):
        """AttLoc forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: previous attention weight (B x T_max)
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights (B x T_max)
        :rtype: torch.Tensor
        """
        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        # initialize attention weight with uniform dist.
        if att_prev is None:
            # if no bias, 0 0-pad goes 0
            att_prev = to_device(self, (1. - make_pad_mask(enc_hs_len).float()))
            att_prev = att_prev / att_prev.new(enc_hs_len).unsqueeze(-1)

        # att_prev: utt x frame -> utt x 1 x 1 x frame -> utt x att_conv_chans x 1 x frame
        att_conv = self.loc_conv(att_prev.view(batch, 1, 1, self.h_length))
        # att_conv: utt x att_conv_chans x 1 x frame -> utt x frame x att_conv_chans
        att_conv = att_conv.squeeze(2).transpose(1, 2)
        # att_conv: utt x frame x att_conv_chans -> utt x frame x att_dim
        att_conv = self.mlp_att(att_conv)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(att_conv + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # weighted sum over flames
        # utt x hdim
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        return c, w


class AttCov(torch.nn.Module):
    """Coverage mechanism attention

    Reference: Get To The Point: Summarization with Pointer-Generator Network
       (https://arxiv.org/abs/1704.04368)

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    """

    def __init__(self, eprojs, dunits, att_dim):
        super(AttCov, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.wvec = torch.nn.Linear(1, att_dim)
        self.gvec = torch.nn.Linear(att_dim, 1)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev_list, scaling=2.0):
        """AttCov forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param list att_prev_list: list of previous attention weight
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weights
        :rtype: list
        """

        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        # initialize attention weight with uniform dist.
        if att_prev_list is None:
            # if no bias, 0 0-pad goes 0
            att_prev_list = to_device(self, (1. - make_pad_mask(enc_hs_len).float()))
            att_prev_list = [att_prev_list / att_prev_list.new(enc_hs_len).unsqueeze(-1)]

        # att_prev_list: L' * [B x T] => cov_vec B x T
        cov_vec = sum(att_prev_list)
        # cov_vec: B x T => B x T x 1 => B x T x att_dim
        cov_vec = self.wvec(cov_vec.unsqueeze(-1))

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(cov_vec + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)
        att_prev_list += [w]

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        return c, att_prev_list


class AttLoc2D(torch.nn.Module):
    """2D location-aware attention

    This attention is an extended version of location aware attention.
    It take not only one frame before attention weights, but also earlier frames into account.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    :param int att_win: attention window size (default=5)
    """

    def __init__(self, eprojs, dunits, att_dim, att_win, aconv_chans, aconv_filts):
        super(AttLoc2D, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.mlp_att = torch.nn.Linear(aconv_chans, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (att_win, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.aconv_chans = aconv_chans
        self.att_win = att_win
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, scaling=2.0):
        """AttLoc2D forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: previous attention weight (B x att_win x T_max)
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights (B x att_win x T_max)
        :rtype: torch.Tensor
        """

        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        # initialize attention weight with uniform dist.
        if att_prev is None:
            # B * [Li x att_win]
            # if no bias, 0 0-pad goes 0
            att_prev = to_device(self, (1. - make_pad_mask(enc_hs_len).float()))
            att_prev = att_prev / att_prev.new(enc_hs_len).unsqueeze(-1)
            att_prev = att_prev.unsqueeze(1).expand(-1, self.att_win, -1)

        # att_prev: B x att_win x Tmax -> B x 1 x att_win x Tmax -> B x C x 1 x Tmax
        att_conv = self.loc_conv(att_prev.unsqueeze(1))
        # att_conv: B x C x 1 x Tmax -> B x Tmax x C
        att_conv = att_conv.squeeze(2).transpose(1, 2)
        # att_conv: utt x frame x att_conv_chans -> utt x frame x att_dim
        att_conv = self.mlp_att(att_conv)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(att_conv + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        # update att_prev: B x att_win x Tmax -> B x att_win+1 x Tmax -> B x att_win x Tmax
        att_prev = torch.cat([att_prev, w.unsqueeze(1)], dim=1)
        att_prev = att_prev[:, 1:]

        return c, att_prev


class AttLocRec(torch.nn.Module):
    """location-aware recurrent attention

    This attention is an extended version of location aware attention.
    With the use of RNN, it take the effect of the history of attention weights into account.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, att_dim, aconv_chans, aconv_filts):
        super(AttLocRec, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.att_lstm = torch.nn.LSTMCell(aconv_chans, att_dim, bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev_states, scaling=2.0):
        """AttLocRec forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param tuple att_prev_states: previous attention weight and lstm states
                                      ((B, T_max), ((B, att_dim), (B, att_dim)))
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights and lstm states (w, (hx, cx))
                 ((B, T_max), ((B, att_dim), (B, att_dim)))
        :rtype: tuple
        """

        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        if att_prev_states is None:
            # initialize attention weight with uniform dist.
            # if no bias, 0 0-pad goes 0
            att_prev = to_device(self, (1. - make_pad_mask(enc_hs_len).float()))
            att_prev = att_prev / att_prev.new(enc_hs_len).unsqueeze(-1)

            # initialize lstm states
            att_h = enc_hs_pad.new_zeros(batch, self.att_dim)
            att_c = enc_hs_pad.new_zeros(batch, self.att_dim)
            att_states = (att_h, att_c)
        else:
            att_prev = att_prev_states[0]
            att_states = att_prev_states[1]

        # B x 1 x 1 x T -> B x C x 1 x T
        att_conv = self.loc_conv(att_prev.view(batch, 1, 1, self.h_length))
        # apply non-linear
        att_conv = F.relu(att_conv)
        # B x C x 1 x T -> B x C x 1 x 1 -> B x C
        att_conv = F.max_pool2d(att_conv, (1, att_conv.size(3))).view(batch, -1)

        att_h, att_c = self.att_lstm(att_conv, att_states)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(att_h.unsqueeze(1) + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        return c, (w, (att_h, att_c))


class AttCovLoc(torch.nn.Module):
    """Coverage mechanism location aware attention

    This attention is a combination of coverage and location-aware attentions.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, att_dim, aconv_chans, aconv_filts):
        super(AttCovLoc, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.mlp_att = torch.nn.Linear(aconv_chans, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)

        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.aconv_chans = aconv_chans
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev_list, scaling=2.0):
        """AttCovLoc forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param list att_prev_list: list of previous attention weight
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weights
        :rtype: list
        """

        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        # initialize attention weight with uniform dist.
        if att_prev_list is None:
            # if no bias, 0 0-pad goes 0
            mask = 1. - make_pad_mask(enc_hs_len).float()
            att_prev_list = [to_device(self, mask / mask.new(enc_hs_len).unsqueeze(-1))]

        # att_prev_list: L' * [B x T] => cov_vec B x T
        cov_vec = sum(att_prev_list)

        # cov_vec: B x T -> B x 1 x 1 x T -> B x C x 1 x T
        att_conv = self.loc_conv(cov_vec.view(batch, 1, 1, self.h_length))
        # att_conv: utt x att_conv_chans x 1 x frame -> utt x frame x att_conv_chans
        att_conv = att_conv.squeeze(2).transpose(1, 2)
        # att_conv: utt x frame x att_conv_chans -> utt x frame x att_dim
        att_conv = self.mlp_att(att_conv)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(att_conv + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)
        att_prev_list += [w]

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        return c, att_prev_list


class AttMultiHeadDot(torch.nn.Module):
    """Multi head dot product attention

    Reference: Attention is all you need
        (https://arxiv.org/abs/1706.03762)

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int aheads: # heads of multi head attention
    :param int att_dim_k: dimension k in multi head attention
    :param int att_dim_v: dimension v in multi head attention
    """

    def __init__(self, eprojs, dunits, aheads, att_dim_k, att_dim_v):
        super(AttMultiHeadDot, self).__init__()
        self.mlp_q = torch.nn.ModuleList()
        self.mlp_k = torch.nn.ModuleList()
        self.mlp_v = torch.nn.ModuleList()
        for _ in six.moves.range(aheads):
            self.mlp_q += [torch.nn.Linear(dunits, att_dim_k)]
            self.mlp_k += [torch.nn.Linear(eprojs, att_dim_k, bias=False)]
            self.mlp_v += [torch.nn.Linear(eprojs, att_dim_v, bias=False)]
        self.mlp_o = torch.nn.Linear(aheads * att_dim_v, eprojs, bias=False)
        self.dunits = dunits
        self.eprojs = eprojs
        self.aheads = aheads
        self.att_dim_k = att_dim_k
        self.att_dim_v = att_dim_v
        self.scaling = 1.0 / math.sqrt(att_dim_k)
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev):
        """AttMultiHeadDot forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: dummy (does not use)
        :return: attention weighted encoder state (B x D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weight (B x T_max) * aheads
        :rtype: list
        """

        batch = enc_hs_pad.size(0)
        # pre-compute all k and v outside the decoder loop
        if self.pre_compute_k is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_k = [
                torch.tanh(self.mlp_k[h](self.enc_h)) for h in six.moves.range(self.aheads)]

        if self.pre_compute_v is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_v = [
                self.mlp_v[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        c = []
        w = []
        for h in six.moves.range(self.aheads):
            e = torch.sum(self.pre_compute_k[h] * torch.tanh(self.mlp_q[h](dec_z)).view(
                batch, 1, self.att_dim_k), dim=2)  # utt x frame

            # NOTE consider zero padding when compute w.
            if self.mask is None:
                self.mask = to_device(self, make_pad_mask(enc_hs_len))
            e.masked_fill_(self.mask, -float('inf'))
            w += [F.softmax(self.scaling * e, dim=1)]

            # weighted sum over flames
            # utt x hdim
            # NOTE use bmm instead of sum(*)
            c += [torch.sum(self.pre_compute_v[h] * w[h].view(batch, self.h_length, 1), dim=1)]

        # concat all of c
        c = self.mlp_o(torch.cat(c, dim=1))

        return c, w


class AttMultiHeadAdd(torch.nn.Module):
    """Multi head additive attention

    Reference: Attention is all you need
        (https://arxiv.org/abs/1706.03762)

    This attention is multi head attention using additive attention for each head.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int aheads: # heads of multi head attention
    :param int att_dim_k: dimension k in multi head attention
    :param int att_dim_v: dimension v in multi head attention
    """

    def __init__(self, eprojs, dunits, aheads, att_dim_k, att_dim_v):
        super(AttMultiHeadAdd, self).__init__()
        self.mlp_q = torch.nn.ModuleList()
        self.mlp_k = torch.nn.ModuleList()
        self.mlp_v = torch.nn.ModuleList()
        self.gvec = torch.nn.ModuleList()
        for _ in six.moves.range(aheads):
            self.mlp_q += [torch.nn.Linear(dunits, att_dim_k)]
            self.mlp_k += [torch.nn.Linear(eprojs, att_dim_k, bias=False)]
            self.mlp_v += [torch.nn.Linear(eprojs, att_dim_v, bias=False)]
            self.gvec += [torch.nn.Linear(att_dim_k, 1)]
        self.mlp_o = torch.nn.Linear(aheads * att_dim_v, eprojs, bias=False)
        self.dunits = dunits
        self.eprojs = eprojs
        self.aheads = aheads
        self.att_dim_k = att_dim_k
        self.att_dim_v = att_dim_v
        self.scaling = 1.0 / math.sqrt(att_dim_k)
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev):
        """AttMultiHeadAdd forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: dummy (does not use)
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weight (B x T_max) * aheads
        :rtype: list
        """

        batch = enc_hs_pad.size(0)
        # pre-compute all k and v outside the decoder loop
        if self.pre_compute_k is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_k = [
                self.mlp_k[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if self.pre_compute_v is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_v = [
                self.mlp_v[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        c = []
        w = []
        for h in six.moves.range(self.aheads):
            e = self.gvec[h](torch.tanh(
                self.pre_compute_k[h] + self.mlp_q[h](dec_z).view(batch, 1, self.att_dim_k))).squeeze(2)

            # NOTE consider zero padding when compute w.
            if self.mask is None:
                self.mask = to_device(self, make_pad_mask(enc_hs_len))
            e.masked_fill_(self.mask, -float('inf'))
            w += [F.softmax(self.scaling * e, dim=1)]

            # weighted sum over flames
            # utt x hdim
            # NOTE use bmm instead of sum(*)
            c += [torch.sum(self.pre_compute_v[h] * w[h].view(batch, self.h_length, 1), dim=1)]

        # concat all of c
        c = self.mlp_o(torch.cat(c, dim=1))

        return c, w


class AttMultiHeadLoc(torch.nn.Module):
    """Multi head location based attention

    Reference: Attention is all you need
        (https://arxiv.org/abs/1706.03762)

    This attention is multi head attention using location-aware attention for each head.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int aheads: # heads of multi head attention
    :param int att_dim_k: dimension k in multi head attention
    :param int att_dim_v: dimension v in multi head attention
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, aheads, att_dim_k, att_dim_v, aconv_chans, aconv_filts):
        super(AttMultiHeadLoc, self).__init__()
        self.mlp_q = torch.nn.ModuleList()
        self.mlp_k = torch.nn.ModuleList()
        self.mlp_v = torch.nn.ModuleList()
        self.gvec = torch.nn.ModuleList()
        self.loc_conv = torch.nn.ModuleList()
        self.mlp_att = torch.nn.ModuleList()
        for _ in six.moves.range(aheads):
            self.mlp_q += [torch.nn.Linear(dunits, att_dim_k)]
            self.mlp_k += [torch.nn.Linear(eprojs, att_dim_k, bias=False)]
            self.mlp_v += [torch.nn.Linear(eprojs, att_dim_v, bias=False)]
            self.gvec += [torch.nn.Linear(att_dim_k, 1)]
            self.loc_conv += [torch.nn.Conv2d(
                1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)]
            self.mlp_att += [torch.nn.Linear(aconv_chans, att_dim_k, bias=False)]
        self.mlp_o = torch.nn.Linear(aheads * att_dim_v, eprojs, bias=False)
        self.dunits = dunits
        self.eprojs = eprojs
        self.aheads = aheads
        self.att_dim_k = att_dim_k
        self.att_dim_v = att_dim_v
        self.scaling = 1.0 / math.sqrt(att_dim_k)
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, scaling=2.0):
        """AttMultiHeadLoc forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: list of previous attention weight (B x T_max) * aheads
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B x D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weight (B x T_max) * aheads
        :rtype: list
        """

        batch = enc_hs_pad.size(0)
        # pre-compute all k and v outside the decoder loop
        if self.pre_compute_k is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_k = [
                self.mlp_k[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if self.pre_compute_v is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_v = [
                self.mlp_v[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        if att_prev is None:
            att_prev = []
            for _ in six.moves.range(self.aheads):
                # if no bias, 0 0-pad goes 0
                mask = 1. - make_pad_mask(enc_hs_len).float()
                att_prev += [to_device(self, mask / mask.new(enc_hs_len).unsqueeze(-1))]

        c = []
        w = []
        for h in six.moves.range(self.aheads):
            att_conv = self.loc_conv[h](att_prev[h].view(batch, 1, 1, self.h_length))
            att_conv = att_conv.squeeze(2).transpose(1, 2)
            att_conv = self.mlp_att[h](att_conv)

            e = self.gvec[h](torch.tanh(
                self.pre_compute_k[h] + att_conv + self.mlp_q[h](dec_z).view(
                    batch, 1, self.att_dim_k))).squeeze(2)

            # NOTE consider zero padding when compute w.
            if self.mask is None:
                self.mask = to_device(self, make_pad_mask(enc_hs_len))
            e.masked_fill_(self.mask, -float('inf'))
            w += [F.softmax(scaling * e, dim=1)]

            # weighted sum over flames
            # utt x hdim
            # NOTE use bmm instead of sum(*)
            c += [torch.sum(self.pre_compute_v[h] * w[h].view(batch, self.h_length, 1), dim=1)]

        # concat all of c
        c = self.mlp_o(torch.cat(c, dim=1))

        return c, w


class AttMultiHeadMultiResLoc(torch.nn.Module):
    """Multi head multi resolution location based attention

    Reference: Attention is all you need
        (https://arxiv.org/abs/1706.03762)

    This attention is multi head attention using location-aware attention for each head.
    Furthermore, it uses different filter size for each head.

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int aheads: # heads of multi head attention
    :param int att_dim_k: dimension k in multi head attention
    :param int att_dim_v: dimension v in multi head attention
    :param int aconv_chans: maximum # channels of attention convolution
        each head use #ch = aconv_chans * (head + 1) / aheads
        e.g. aheads=4, aconv_chans=100 => filter size = 25, 50, 75, 100
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, aheads, att_dim_k, att_dim_v, aconv_chans, aconv_filts):
        super(AttMultiHeadMultiResLoc, self).__init__()
        self.mlp_q = torch.nn.ModuleList()
        self.mlp_k = torch.nn.ModuleList()
        self.mlp_v = torch.nn.ModuleList()
        self.gvec = torch.nn.ModuleList()
        self.loc_conv = torch.nn.ModuleList()
        self.mlp_att = torch.nn.ModuleList()
        for h in six.moves.range(aheads):
            self.mlp_q += [torch.nn.Linear(dunits, att_dim_k)]
            self.mlp_k += [torch.nn.Linear(eprojs, att_dim_k, bias=False)]
            self.mlp_v += [torch.nn.Linear(eprojs, att_dim_v, bias=False)]
            self.gvec += [torch.nn.Linear(att_dim_k, 1)]
            afilts = aconv_filts * (h + 1) // aheads
            self.loc_conv += [torch.nn.Conv2d(
                1, aconv_chans, (1, 2 * afilts + 1), padding=(0, afilts), bias=False)]
            self.mlp_att += [torch.nn.Linear(aconv_chans, att_dim_k, bias=False)]
        self.mlp_o = torch.nn.Linear(aheads * att_dim_v, eprojs, bias=False)
        self.dunits = dunits
        self.eprojs = eprojs
        self.aheads = aheads
        self.att_dim_k = att_dim_k
        self.att_dim_v = att_dim_v
        self.scaling = 1.0 / math.sqrt(att_dim_k)
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_k = None
        self.pre_compute_v = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev):
        """AttMultiHeadMultiResLoc forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: list of previous attention weight (B x T_max) * aheads
        :return: attention weighted encoder state (B x D_enc)
        :rtype: torch.Tensor
        :return: list of previous attention weight (B x T_max) * aheads
        :rtype: list
        """

        batch = enc_hs_pad.size(0)
        # pre-compute all k and v outside the decoder loop
        if self.pre_compute_k is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_k = [
                self.mlp_k[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if self.pre_compute_v is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_v = [
                self.mlp_v[h](self.enc_h) for h in six.moves.range(self.aheads)]

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        if att_prev is None:
            att_prev = []
            for _ in six.moves.range(self.aheads):
                # if no bias, 0 0-pad goes 0
                mask = 1. - make_pad_mask(enc_hs_len).float()
                att_prev += [to_device(self, mask / mask.new(enc_hs_len).unsqueeze(-1))]

        c = []
        w = []
        for h in six.moves.range(self.aheads):
            att_conv = self.loc_conv[h](att_prev[h].view(batch, 1, 1, self.h_length))
            att_conv = att_conv.squeeze(2).transpose(1, 2)
            att_conv = self.mlp_att[h](att_conv)

            e = self.gvec[h](torch.tanh(
                self.pre_compute_k[h] + att_conv + self.mlp_q[h](dec_z).view(
                    batch, 1, self.att_dim_k))).squeeze(2)

            # NOTE consider zero padding when compute w.
            if self.mask is None:
                self.mask = to_device(self, make_pad_mask(enc_hs_len))
            e.masked_fill_(self.mask, -float('inf'))
            w += [F.softmax(self.scaling * e, dim=1)]

            # weighted sum over flames
            # utt x hdim
            # NOTE use bmm instead of sum(*)
            c += [torch.sum(self.pre_compute_v[h] * w[h].view(batch, self.h_length, 1), dim=1)]

        # concat all of c
        c = self.mlp_o(torch.cat(c, dim=1))

        return c, w


class AttForward(torch.nn.Module):
    """Forward attention

    Reference: Forward attention in sequence-to-sequence acoustic modeling for speech synthesis
        (https://arxiv.org/pdf/1807.06736.pdf)

    :param int eprojs: # projection-units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    """

    def __init__(self, eprojs, dunits, att_dim, aconv_chans, aconv_filts):
        super(AttForward, self).__init__()
        self.mlp_enc = torch.nn.Linear(eprojs, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.mlp_att = torch.nn.Linear(aconv_chans, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)
        self.dunits = dunits
        self.eprojs = eprojs
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def reset(self):
        """reset states"""
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, scaling=1.0):
        """AttForward forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B x T_max x D_enc)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B x D_dec)
        :param torch.Tensor att_prev: attention weights of previous step
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, D_enc)
        :rtype: torch.Tensor
        :return: previous attention weights (B x T_max)
        :rtype: torch.Tensor
        """
        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        if att_prev is None:
            # initial attention will be [1, 0, 0, ...]
            att_prev = enc_hs_pad.new_zeros(*enc_hs_pad.size()[:2])
            att_prev[:, 0] = 1.0

        # att_prev: utt x frame -> utt x 1 x 1 x frame -> utt x att_conv_chans x 1 x frame
        att_conv = self.loc_conv(att_prev.view(batch, 1, 1, self.h_length))
        # att_conv: utt x att_conv_chans x 1 x frame -> utt x frame x att_conv_chans
        att_conv = att_conv.squeeze(2).transpose(1, 2)
        # att_conv: utt x frame x att_conv_chans -> utt x frame x att_dim
        att_conv = self.mlp_att(att_conv)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).unsqueeze(1)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(self.pre_compute_enc_h + dec_z_tiled + att_conv)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # forward attention
        att_prev_shift = F.pad(att_prev, (1, 0))[:, :-1]
        w = (att_prev + att_prev_shift) * w
        # NOTE: clamp is needed to avoid nan gradient
        w = F.normalize(torch.clamp(w, 1e-6), p=1, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.unsqueeze(-1), dim=1)

        return c, w


class AttForwardTA(torch.nn.Module):
    """Forward attention with transition agent

    Reference: Forward attention in sequence-to-sequence acoustic modeling for speech synthesis
        (https://arxiv.org/pdf/1807.06736.pdf)

    :param int eunits: # units of encoder
    :param int dunits: # units of decoder
    :param int att_dim: attention dimension
    :param int aconv_chans: # channels of attention convolution
    :param int aconv_filts: filter size of attention convolution
    :param int odim: output dimension
    """

    def __init__(self, eunits, dunits, att_dim, aconv_chans, aconv_filts, odim):
        super(AttForwardTA, self).__init__()
        self.mlp_enc = torch.nn.Linear(eunits, att_dim)
        self.mlp_dec = torch.nn.Linear(dunits, att_dim, bias=False)
        self.mlp_ta = torch.nn.Linear(eunits + dunits + odim, 1)
        self.mlp_att = torch.nn.Linear(aconv_chans, att_dim, bias=False)
        self.loc_conv = torch.nn.Conv2d(
            1, aconv_chans, (1, 2 * aconv_filts + 1), padding=(0, aconv_filts), bias=False)
        self.gvec = torch.nn.Linear(att_dim, 1)
        self.dunits = dunits
        self.eunits = eunits
        self.att_dim = att_dim
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None
        self.trans_agent_prob = 0.5

    def reset(self):
        self.h_length = None
        self.enc_h = None
        self.pre_compute_enc_h = None
        self.mask = None
        self.trans_agent_prob = 0.5

    def forward(self, enc_hs_pad, enc_hs_len, dec_z, att_prev, out_prev, scaling=1.0):
        """AttForwardTA forward

        :param torch.Tensor enc_hs_pad: padded encoder hidden state (B, Tmax, eunits)
        :param list enc_hs_len: padded encoder hidden state length (B)
        :param torch.Tensor dec_z: decoder hidden state (B, dunits)
        :param torch.Tensor att_prev: attention weights of previous step
        :param torch.Tensor out_prev: decoder outputs of previous step (B, odim)
        :param float scaling: scaling parameter before applying softmax
        :return: attention weighted encoder state (B, dunits)
        :rtype: torch.Tensor
        :return: previous attention weights (B, Tmax)
        :rtype: torch.Tensor
        """
        batch = len(enc_hs_pad)
        # pre-compute all h outside the decoder loop
        if self.pre_compute_enc_h is None:
            self.enc_h = enc_hs_pad  # utt x frame x hdim
            self.h_length = self.enc_h.size(1)
            # utt x frame x att_dim
            self.pre_compute_enc_h = self.mlp_enc(self.enc_h)

        if dec_z is None:
            dec_z = enc_hs_pad.new_zeros(batch, self.dunits)
        else:
            dec_z = dec_z.view(batch, self.dunits)

        if att_prev is None:
            # initial attention will be [1, 0, 0, ...]
            att_prev = enc_hs_pad.new_zeros(*enc_hs_pad.size()[:2])
            att_prev[:, 0] = 1.0

        # att_prev: utt x frame -> utt x 1 x 1 x frame -> utt x att_conv_chans x 1 x frame
        att_conv = self.loc_conv(att_prev.view(batch, 1, 1, self.h_length))
        # att_conv: utt x att_conv_chans x 1 x frame -> utt x frame x att_conv_chans
        att_conv = att_conv.squeeze(2).transpose(1, 2)
        # att_conv: utt x frame x att_conv_chans -> utt x frame x att_dim
        att_conv = self.mlp_att(att_conv)

        # dec_z_tiled: utt x frame x att_dim
        dec_z_tiled = self.mlp_dec(dec_z).view(batch, 1, self.att_dim)

        # dot with gvec
        # utt x frame x att_dim -> utt x frame
        e = self.gvec(torch.tanh(att_conv + self.pre_compute_enc_h + dec_z_tiled)).squeeze(2)

        # NOTE consider zero padding when compute w.
        if self.mask is None:
            self.mask = to_device(self, make_pad_mask(enc_hs_len))
        e.masked_fill_(self.mask, -float('inf'))
        w = F.softmax(scaling * e, dim=1)

        # forward attention
        att_prev_shift = F.pad(att_prev, (1, 0))[:, :-1]
        w = (self.trans_agent_prob * att_prev + (1 - self.trans_agent_prob) * att_prev_shift) * w
        # NOTE: clamp is needed to avoid nan gradient
        w = F.normalize(torch.clamp(w, 1e-6), p=1, dim=1)

        # weighted sum over flames
        # utt x hdim
        # NOTE use bmm instead of sum(*)
        c = torch.sum(self.enc_h * w.view(batch, self.h_length, 1), dim=1)

        # update transition agent prob
        self.trans_agent_prob = torch.sigmoid(
            self.mlp_ta(torch.cat([c, out_prev, dec_z], dim=1)))

        return c, w


def att_for(args, num_att=1):
    """Instantiates an attention module given the program arguments

    :param Namespace args: The arguments
    :param int num_att: number of attention modules (in multi-speaker case, it can be 2 or more)
    :rtype torch.nn.Module
    :return: The attention module
    """
    att_list = torch.nn.ModuleList()
    for i in range(num_att):
        att = None
        if args.atype == 'noatt':
            att = NoAttention()
        elif args.atype == 'dot':
            att = AttDot(args.eprojs, args.dunits, args.adim)
        elif args.atype == 'add':
            att = AttAdd(args.eprojs, args.dunits, args.adim)
        elif args.atype == 'location':
            att = AttLoc(args.eprojs, args.dunits,
                         args.adim, args.aconv_chans, args.aconv_filts)
        elif args.atype == 'location2d':
            att = AttLoc2D(args.eprojs, args.dunits,
                           args.adim, args.awin, args.aconv_chans, args.aconv_filts)
        elif args.atype == 'location_recurrent':
            att = AttLocRec(args.eprojs, args.dunits,
                            args.adim, args.aconv_chans, args.aconv_filts)
        elif args.atype == 'coverage':
            att = AttCov(args.eprojs, args.dunits, args.adim)
        elif args.atype == 'coverage_location':
            att = AttCovLoc(args.eprojs, args.dunits, args.adim,
                            args.aconv_chans, args.aconv_filts)
        elif args.atype == 'multi_head_dot':
            att = AttMultiHeadDot(args.eprojs, args.dunits,
                                  args.aheads, args.adim, args.adim)
        elif args.atype == 'multi_head_add':
            att = AttMultiHeadAdd(args.eprojs, args.dunits,
                                  args.aheads, args.adim, args.adim)
        elif args.atype == 'multi_head_loc':
            att = AttMultiHeadLoc(args.eprojs, args.dunits,
                                  args.aheads, args.adim, args.adim,
                                  args.aconv_chans, args.aconv_filts)
        elif args.atype == 'multi_head_multi_res_loc':
            att = AttMultiHeadMultiResLoc(args.eprojs, args.dunits,
                                          args.aheads, args.adim, args.adim,
                                          args.aconv_chans, args.aconv_filts)
        att_list.append(att)
    return att_list


def att_to_numpy(att_ws, att):
    """Converts attention weights to a numpy array given the attention

    :param list att_ws: The attention weights
    :param torch.nn.Module att: The attention
    :rtype: np.ndarray
    :return: The numpy array of the attention weights
    """
    # convert to numpy array with the shape (B, Lmax, Tmax)
    if isinstance(att, AttLoc2D):
        # att_ws => list of previous concate attentions
        att_ws = torch.stack([aw[:, -1] for aw in att_ws], dim=1).cpu().numpy()
    elif isinstance(att, (AttCov, AttCovLoc)):
        # att_ws => list of list of previous attentions
        att_ws = torch.stack([aw[-1] for aw in att_ws], dim=1).cpu().numpy()
    elif isinstance(att, AttLocRec):
        # att_ws => list of tuple of attention and hidden states
        att_ws = torch.stack([aw[0] for aw in att_ws], dim=1).cpu().numpy()
    elif isinstance(att, (AttMultiHeadDot, AttMultiHeadAdd, AttMultiHeadLoc, AttMultiHeadMultiResLoc)):
        # att_ws => list of list of each head attention
        n_heads = len(att_ws[0])
        att_ws_sorted_by_head = []
        for h in six.moves.range(n_heads):
            att_ws_head = torch.stack([aw[h] for aw in att_ws], dim=1)
            att_ws_sorted_by_head += [att_ws_head]
        att_ws = torch.stack(att_ws_sorted_by_head, dim=1).cpu().numpy()
    else:
        # att_ws => list of attentions
        att_ws = torch.stack(att_ws, dim=1).cpu().numpy()
    return att_ws
