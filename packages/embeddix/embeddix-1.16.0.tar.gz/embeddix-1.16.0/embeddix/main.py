"""Welcome to embeddix.

This is the entry point of the application.
"""
import os

import argparse
import logging
import logging.config

import embeddix.core.converter as converter
import embeddix.core.extractor as extractor
import embeddix.core.evaluator as evaluator
import embeddix.core.reducer as reducer
import embeddix.utils.config as cutils


logging.config.dictConfig(
    cutils.load(
        os.path.join(os.path.dirname(__file__), 'logging', 'logging.yml')))

logger = logging.getLogger(__name__)


def _reduce(args):
    reducer.align_vocabs_and_models(args.embeddings)


def _convert(args):
    if args.to == 'numpy':
        if not args.embeddings.endswith('.txt'):
            raise Exception('Invalid input file: should be a text file '
                            'ending with .txt')
        converter.convert_to_numpy(args.embeddings)
    else:
        if not args.embeddings.endswith('.npy'):
            raise Exception('Invalid input file: should be a numpy file '
                            'ending with .npy')
        if not args.vocab:
            raise Exception('Converting to txt requires specifying the '
                            '--vocab parameter')
        converter.convert_to_txt(args.embeddings, args.vocab)


def _extract(args):
    extractor.extract_vocab(args.embeddings)


def _evaluate(args):
    logger.info('Loading distributional space from {}'.format(args.embeddings))
    evaluator.evaluate_distributional_space(args.embeddings, args.vocab,
                                            args.dataset)


def main():
    """Launch embeddix."""
    parser = argparse.ArgumentParser(prog='embeddix')
    subparsers = parser.add_subparsers()
    parser_extract = subparsers.add_parser(
        'extract', formatter_class=argparse.RawTextHelpFormatter,
        help='extract vocab from embeddings txt file')
    parser_extract.set_defaults(func=_extract)
    parser_extract.add_argument('-e', '--embeddings', required=True,
                                help='input embedding in txt format')
    parser_convert = subparsers.add_parser(
        'convert', formatter_class=argparse.RawTextHelpFormatter,
        help='convert embeddings to and from numpy and txt formats')
    parser_convert.set_defaults(func=_convert)
    parser_convert.add_argument('-t', '--to', choices=['numpy', 'txt'],
                                help='output format: numpy or text')
    parser_convert.add_argument('-v', '--vocab',
                                help='absolute path to vocabulary')
    parser_convert.add_argument('-e', '--embeddings', required=True,
                                help='absolute path to embeddings file')
    parser_evaluate = subparsers.add_parser(
        'evaluate', formatter_class=argparse.RawTextHelpFormatter,
        help='evaluate embeddings model on various intrinsic tasks')
    parser_evaluate.set_defaults(func=_evaluate)
    parser_evaluate.add_argument('-e', '--embeddings', required=True,
                                 help='absolute path to .npy embeddings')
    parser_evaluate.add_argument('-v', '--vocab', required=True,
                                 help='absolute path to .vocab file')
    parser_evaluate.add_argument('-d', '--dataset', required=True,
                                 choices=['ap', 'battig', 'essli', 'men',
                                          'simlex', 'simverb'],
                                 help='which dataset to evaluate on')
    args = parser.parse_args()
    args.func(args)
