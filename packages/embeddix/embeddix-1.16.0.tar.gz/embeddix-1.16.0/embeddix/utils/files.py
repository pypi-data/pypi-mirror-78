"""Files utils."""
import logging

import numpy as np

from scipy import sparse

__all__ = ('save_vocab', 'load_vocab', 'count_lines',
           'load_sparse', 'save_sparse', 'save_dense', 'get_shared_vocab',
           'save_counts', 'load_counts')

logger = logging.getLogger(__name__)


def load_counts(counts_filepath):
    """Load word counts dict from file."""
    counts = {}
    with open(counts_filepath, 'r', encoding='utf-8') as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            counts[linesplit[0]] = int(linesplit[1])
    return counts


def save_counts(counts_filepath, counts):
    """Save word counts dict to file."""
    with open(counts_filepath, 'w', encoding='utf-8') as counts_str:
        for word, count in sorted(counts.items(), key=lambda x: x[1],
                                  reverse=True):
            print('{}\t{}'.format(word, count), file=counts_str)


def load_dense(matrix_filepath):
    """Load numpy dense matrix."""
    return np.load(matrix_filepath)


def load_sparse(matrix_filepath):
    """Load scipy sparse matrix."""
    return sparse.load_npz(matrix_filepath)


def save_sparse(matrix_filepath, matrix):
    """Save scipy sparse matrix to file."""
    logger.info('Saving scipy sparse matrix to {}'.format(matrix_filepath))
    sparse.save_npz(matrix_filepath, matrix)


def save_dense(matrix_filepath, matrix):
    """Save numpy dense matrix to file."""
    logger.info('Saving numpy dense matrix to {}'.format(matrix_filepath))
    np.save(matrix_filepath, matrix)


def save_vocab(vocab_filepath, vocab):
    """Save vocabulary to file."""
    logger.info('Saving vocabulary to {}'.format(vocab_filepath))
    with open(vocab_filepath, 'w', encoding='utf-8') as vocab_stream:
        for word, idx in vocab.items():
            print('{}\t{}'.format(idx, word), file=vocab_stream)


def load_vocab(vocab_filepath):
    """Load word_to_idx dict mapping from .vocab filepath."""
    word_to_idx = {}
    logger.info('Loading vocabulary from {}'.format(vocab_filepath))
    with open(vocab_filepath, 'r', encoding='utf-8') as input_stream:
        for line in input_stream:
            linesplit = line.strip().split('\t')
            word_to_idx[linesplit[1]] = int(linesplit[0])
    return word_to_idx


def count_lines(input_filepath):
    """Count number of non-empty lines in file."""
    counter = 0
    with open(input_filepath, 'r', encoding='utf-8') as input_str:
        for line in input_str:
            if line.strip():
                counter += 1
    return counter


def get_shared_vocab(vocab1, vocab2):
    """Return intersection of two vocabs."""
    shared_words = set(word for word in vocab1 if word in vocab2)
    return {word: idx for idx, word in enumerate(shared_words)}
