"""
Utilities related to using reldi in the pipeline.
"""
from classla.models.common import conll


def check_reldi():
    """
    Import necessary components from reldi to perform tokenization.
    """
    try:
        import classla
    except ImportError:
        raise ImportError(
            "Reldi is used but not present on your machine. Make sure you run 'git submodule init' and 'git submodule update' commands."
        )
    return True


class ReldiTokenizer():
    def __init__(self, lang='sl', type='standard'):
        """ Construct a reldi-based tokenizer by loading the reldi pipeline.
        """
        if lang not in ['sl', 'hr', 'sr', 'bg', 'mk']:
            raise Exception("Reldi tokenizer is currently only allowed in Slovene, Croatian and Serbian pipelines.")

        check_reldi()
        from classla.submodules.reldi_tokeniser import tokeniser
        self.nlp = tokeniser
        self.lang = lang
        self.type = type

    def _reldi_tokenizer(self, input, par_id):
        """
        Slightly modified function reldi_tokeniser.represent_tomaz. Modifications include:

        1.) Erase of non conllu format options (not relevant for pipeline).

        Original function not used because it uses args, which is not passed as parameter.
        """
        output = ''
        sent_id = 0
        output += '# newpar id = ' + str(par_id) + '\n'
        for sent_idx, sent in enumerate(input):
            sent_id += 1
            token_id = 0
            output += '# sent_id = ' + str(par_id) + '.' + str(sent_id) + '\n'
            output += '# text = ' + self.nlp.to_text(sent)
            for token_idx, (token, start, end) in enumerate(sent):
                if not token[0].isspace():
                    token_id += 1
                    SpaceAfter = True
                    if len(sent) > token_idx + 1:
                        SpaceAfter = sent[token_idx + 1][0].isspace()
                    elif len(input) > sent_idx + 1:
                        SpaceAfter = input[sent_idx + 1][0][0].isspace()
                    if SpaceAfter:
                        output += str(token_id) + '\t' + token + '\t_' * 8 + '\n'
                    else:
                        output += str(token_id) + '\t' + token + '\t_' * 7 + '\tSpaceAfter=No\n'
            output += '\n'
        return output


    def tokenize(self, document):
        """ Tokenize a document with the reldi tokenizer and add results to document.conll_file.
        """
        raw_text = '\n'.join(document.text) if isinstance(document.text, list) else document.text
        conllu_output_string = ''
        tokenizer = self.nlp.generate_tokenizer(self.lang)
        for par_id, text in enumerate(raw_text.split('\n')):
            conllu_output_string += self._reldi_tokenizer(self.nlp.process[self.type](tokenizer, text, self.lang), par_id + 1)

        document.conll_file = conll.CoNLLFile(input_str=conllu_output_string)
