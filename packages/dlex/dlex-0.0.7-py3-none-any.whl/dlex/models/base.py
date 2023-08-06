import abc
import itertools
import os
from dataclasses import dataclass

import torch
import torch.nn as nn

from torch.utils.losses import nll_loss
from ..utils.model_utils import get_optimizer


@dataclass
class BatchItem:
    X: torch.Tensor
    Y: torch.Tensor
    X_len: torch.Tensor = None
    Y_len: torch.Tensor = None


@dataclass
class Batch:
    X: torch.Tensor
    Y: torch.Tensor
    X_len: list = None
    Y_len: list = None

    def __getitem__(self, i: int) -> BatchItem:
        return BatchItem(X=self.X[i], X_len=self.X_len and self.X_len[i], Y=self.Y[i], Y_len=self.Y_len and self.Y_len[i])


class BaseModel(torch.nn.Module):
    def __init__(self, params, dataset):
        super().__init__()
        self.params = params
        self.dataset = dataset

        self.global_step = 0
        self.current_epoch = 0

        if torch.cuda.is_available():
            # logger.info("Cuda available: %s", torch.cuda.get_device_name(0))
            self.cuda()

        self._optimizers = None
        self._loss_fn = None

    @property
    def optimizers(self):
        if self._optimizers is None:
            self._optimizers = [get_optimizer(self.params.train.optimizer, self.parameters())]
        return self._optimizers

    @property
    def loss_fn(self):
        if self._loss_fn is None:
            raise Exception("Loss function must be assigned")
        return self._loss_fn

    @property
    def cfg(self):
        # Model configs
        return self.params.model

    def load(self, tag):
        path = os.path.join("saved_models", self.params.path, tag + ".pt")
        self.load_state_dict(torch.load(path))

    @property
    def epoch(self):
        return self.global_step / len(self.dataset)

    @abc.abstractmethod
    def infer(self, batch: Batch):
        """Infer"""
        return None

    def training_step(self, batch: Batch):
        self.zero_grad()
        output = self.forward(batch)
        loss = self.get_loss(batch, output)
        loss.backward()
        for optimizer in self.optimizers:
            if self.params.train.max_grad_norm is not None and self.params.train.max_grad_norm > 0:
                params = itertools.chain.from_iterable([group['params'] for group in optimizer.param_groups])
                nn.utils.clip_grad_norm_(params, self.params.train.max_grad_norm)
            optimizer.step()
        return loss

    def write_summary(self, summary_writer, batch, output):
        pass


class ClassificationBaseModel(BaseModel):
    def __init__(self, params, dataset):
        super().__init__(params, dataset)

    def infer(self, batch):
        logits = self.forward(batch)
        return torch.max(logits, 1)[1], None

    @staticmethod
    def get_loss(batch: Batch, output):
        return nll_loss(batch, output)


def default_params(default):
    def wrap_fn(cls):
        class wrap_cls(cls):
            def __init__(self, params, dataset):
                params.model.extend_default_keys(default)
                super().__init__(params, dataset)
        return wrap_cls
    return wrap_fn
