"""
Processor for performing dependency parsing
"""

from classla.models.common.pretrain import Pretrain
from classla.models.common.utils import unsort
from classla.models.depparse.data import DataLoader
from classla.models.depparse.trainer import Trainer
from classla.pipeline._constants import *
from classla.pipeline.processor import UDProcessor


class DepparseProcessor(UDProcessor):

    # set of processor requirements this processor fulfills
    PROVIDES_DEFAULT = set([DEPPARSE])
    # set of processor requirements for this processor
    REQUIRES_DEFAULT = set([TOKENIZE, POS])

    def _set_up_model(self, config, use_gpu):
        self._pretrain = Pretrain(config['pretrain_path'])
        self._trainer = Trainer(pretrain=self.pretrain, model_file=config['model_path'], use_cuda=use_gpu)

    def process(self, doc):
        batch = DataLoader(
            doc, self.config['batch_size'], self.config, self.pretrain, vocab=self.vocab, evaluation=True,
            sort_during_eval=True)
        preds = []
        for i, b in enumerate(batch):
            preds += self.trainer.predict(b)
        preds = unsort(preds, batch.data_orig_idx)
        batch.conll.set(['head', 'deprel'], [y for x in preds for y in x])
