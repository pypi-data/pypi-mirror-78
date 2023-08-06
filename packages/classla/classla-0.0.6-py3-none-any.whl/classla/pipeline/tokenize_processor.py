"""
Processor for performing tokenization
"""

from classla.models.common import conll
from classla.pipeline._constants import *
from classla.pipeline.processor import UDProcessor


# class for running the tokenizer
from classla.utils.reldi import ReldiTokenizer


class TokenizeProcessor(UDProcessor):

    # set of processor requirements this processor fulfills
    PROVIDES_DEFAULT = set([TOKENIZE])
    # set of processor requirements for this processor
    REQUIRES_DEFAULT = set([])
    # default max sequence length
    MAX_SEQ_LENGTH_DEFAULT = 1000

    def _set_up_model(self, config, use_gpu):
        # set up trainer
        self._reldi_tokenizer = ReldiTokenizer(config.get('lang'), config.get('type'))
        if config.get('pretokenized'):
            self._trainer = None

    def process_pre_tokenized_text(self, doc):
        """
        Pretokenized text can be provided in 2 manners:

        1.) str, tokenized by whitespace, sentence split by newline
        2.) list of token lists, each token list represents a sentence

        generate CoNLL-U output
        """
        conllu_output_string = ""

        # TODO: This was added for input, that is already in CoNLL-U format.
        #       The conll_file attribute is added manually do the Document instance in that case.
        if doc.text is None:
            return

        if isinstance(doc.text, str):
            sentences = [sent.rstrip(' ').split() for sent in doc.text.rstrip('\n').split('\n') if sent]
        elif isinstance(doc.text, list):
            sentences = doc.text
        for sentence in sentences:
            for token_id, token in enumerate(sentence):
                conllu_data = ['_'] * conll.FIELD_NUM
                conllu_data[conll.FIELD_TO_IDX['id']] = str(token_id + 1)
                conllu_data[conll.FIELD_TO_IDX['word']] = token
                conllu_data[conll.FIELD_TO_IDX['head']] = str(token_id)
                conllu_output_string += ('\t'.join(conllu_data)+'\n')
            conllu_output_string += '\n'
        doc.conll_file = conll.CoNLLFile(input_str=conllu_output_string)

    def process(self, document):
        if self.config.get('pretokenized'):
            self.process_pre_tokenized_text(document)
        else:
            return self._reldi_tokenizer.tokenize(document)
