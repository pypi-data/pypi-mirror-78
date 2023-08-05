"""Reduce size of embeddings by aligning their vocabularies."""
import os
import logging

import numpy as np

from scipy import sparse
from tqdm import tqdm

import embeddix.utils.files as futils

__all__ = ('reduce_sparse', 'reduce_dense')

logger = logging.getLogger(__name__)


# pylint: disable=C0103
def reduce_sparse(model, vocab, shared_vocab):
    """Reduce a sparse CSR matrix from vocab to shared_vocab (rows + columns)."""
    rows = []
    columns = []
    data = []
    model = model.tocoo()
    idx2word = {idx: word for word, idx in vocab.items()}
    for i, j, v in tqdm(zip(model.row, model.col, model.data),
                        total=len(model.data)):
        if idx2word[i] in shared_vocab and idx2word[j] in shared_vocab:
            rows.append(shared_vocab[idx2word[i]])
            columns.append(shared_vocab[idx2word[j]])
            data.append(v)
    return sparse.csr_matrix((data, (rows, columns)),
                             shape=(len(shared_vocab),
                                    len(shared_vocab)),
                             dtype='f')


def reduce_dense(model, vocab, shared_vocab):
    """Reduce a dense ndarray from vocab to shared_vocab (rows only)."""
    _model = np.empty(shape=(len(shared_vocab), model.shape[1]))
    idx2word = {idx: word for word, idx in shared_vocab.items()}
    for idx, word in idx2word.items():
        _model[idx] = model[vocab[word]]
    return _model


# TODO: refactor?
def align_vocabs_and_models(embeddings_dirpath):
    """Align all models under dirpath on the same vocabulary."""
    logger.info('Aligning vocabularies under {}'
                .format(embeddings_dirpath))
    shared_vocab = futils.load_shared_vocab(embeddings_dirpath)
    logger.info('Shared vocabulary size = {}'.format(len(shared_vocab)))
    model_names = [filename.split('.npy')[0] for filename in
                   os.listdir(embeddings_dirpath) if filename.endswith('.npy')]
    logger.info('Processing models = {}'.format(model_names))
    for model_name in model_names:
        model_filepath = os.path.join(embeddings_dirpath,
                                      '{}.npy'.format(model_name))
        model = np.load(model_filepath)
        vocab_filepath = os.path.join(embeddings_dirpath,
                                      '{}.vocab'.format(model_name))
        vocab = futils.load_vocab(vocab_filepath)
        reduced_model = reduce_dense(model, vocab, shared_vocab)
        reduced_model_filepath = os.path.join(embeddings_dirpath,
                                              '{}-reduced'.format(model_name))
        np.save(reduced_model_filepath, reduced_model)
        reduced_vocab_filepath = os.path.join(
            embeddings_dirpath, '{}-reduced.vocab'.format(model_name))
        with open(reduced_vocab_filepath, 'w', encoding='utf-8') as output_str:
            for word, idx in shared_vocab.items():
                print('{}\t{}'.format(idx, word), file=output_str)
