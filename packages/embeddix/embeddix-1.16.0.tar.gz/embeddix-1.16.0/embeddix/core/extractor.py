"""Extract vocabulary from txt embeddings."""
import logging

from tqdm import tqdm

import embeddix.utils.files as futils

__all__ = ('extract_vocab')

logger = logging.getLogger(__name__)


def extract_vocab(embeddings_filepath):
    """Extract vocabulary from text embeddings."""
    words = []
    logger.info('Extracting vocabulary from {}'.format(embeddings_filepath))
    with open(embeddings_filepath, 'r', encoding='utf-8') as m_stream:
        for line in tqdm(m_stream,
                         total=futils.count_lines(embeddings_filepath)):
            line = line.strip()
            word = line.split(' ')[0]
            words.append(word)
    vocab_filepath = '{}.vocab'.format(embeddings_filepath.split('.txt')[0])
    with open(vocab_filepath, 'w', encoding='utf-8') as v_stream:
        for idx, word in enumerate(words):
            print('{}\t{}'.format(idx, word), file=v_stream)
    logger.info('Extracted {} words'.format(len(words)))
