"""Convert embeddings to various formats."""
import logging

import numpy as np
from tqdm import tqdm

import embeddix.utils.files as futils

__all__ = ('convert_to_numpy', 'convert_to_txt')

logger = logging.getLogger(__name__)


def convert_to_txt(embeddings_filepath, vocab_filepath):
    """Convert numpy embeddings to text."""
    logger.info('Converting input numpy file to txt: {}'
                .format(embeddings_filepath))
    vocab = futils.load_vocab(vocab_filepath)
    model = np.load(embeddings_filepath)
    txt_model_filepath = '{}.txt'.format(embeddings_filepath.split('.npy')[0])
    logger.info('Saving output to {}'.format(txt_model_filepath))
    with open(txt_model_filepath, 'w', encoding='utf-8') as otp:
        for word, idx in vocab.items():
            vector = ' '.join([str(item) for item in model[idx].tolist()])
            print('{} {}'.format(word, vector), file=otp)


def _convert_to_numpy(words, vectors, output_filepath):
    logger.info('Saving numpy vectors to {}.npy'.format(output_filepath))
    np.save(output_filepath, vectors)
    vocab_filepath = '{}.vocab'.format(output_filepath)
    logger.info('Saving vocabulary to {}'.format(vocab_filepath))
    with open(vocab_filepath, 'w', encoding='utf-8') as vocab_stream:
        for idx, word in enumerate(words):
            print('{}\t{}'.format(idx, word), file=vocab_stream)


def _extract_words_and_vectors_from_txt(embeddings_filepath):
    words = []
    vectors = None
    with open(embeddings_filepath, 'r', encoding='utf-8') as input_str:
        for line in tqdm(input_str,
                         total=futils.count_lines(embeddings_filepath)):
            line = line.strip()
            if line:
                tokens = line.split(' ', 1)
                key = tokens[0].lower()
                words.append(key)
                value = np.fromstring(tokens[1], dtype='float32', sep=' ')
                if not np.any(vectors):
                    vectors = value
                else:
                    vectors = np.vstack((vectors, value))
    return words, vectors


def convert_to_numpy(embeddings_filepath):
    """Convert text embeddings to numpy."""
    logger.info('Converting input txt file to numpy: {}'
                .format(embeddings_filepath))
    output_filepath = '{}'.format(embeddings_filepath.split('.txt')[0])
    words, vectors = _extract_words_and_vectors_from_txt(embeddings_filepath)
    _convert_to_numpy(words, vectors, output_filepath)
