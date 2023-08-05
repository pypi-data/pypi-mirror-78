"""Evaluation metrics utilities."""

import logging
import numpy as np
import scipy.stats as stats

logger = logging.getLogger(__name__)

__all__ = ('purity', 'spearman', 'similarity', 'rmse', 'pearson', 'hmean',
           'energy')


# pylint: disable=C0103,W0622
def purity(y_true, y_pred):
    """Calculate purity for given true and predicted cluster labels.

    Parameters
    ----------
    y_true: array, shape: (n_samples, 1)
      True cluster labels
    y_pred: array, shape: (n_samples, 1)
      Cluster assingment.

    Returns
    -------
    purity: float
      Calculated purity.

    """
    assert len(y_true) == len(y_pred)
    true_clusters = np.zeros(shape=(len(set(y_true)), len(y_true)))
    pred_clusters = np.zeros_like(true_clusters)
    for id, cl in enumerate(set(y_true)):
        true_clusters[id] = (y_true == cl).astype('int')
    for id, cl in enumerate(set(y_pred)):
        pred_clusters[id] = (y_pred == cl).astype('int')
    M = pred_clusters.dot(true_clusters.T)
    return 1. / len(y_true) * np.sum(np.max(M, axis=1))


def hmean(values):
    """Return harmonic mean of values."""
    return stats.hmean(values)


def rmse(x, y):
    """Return root mean squared error."""
    return np.sqrt(((x - y) ** 2).mean())


# pylint: disable=C0103
def spearman(x, y):
    """Compute Spearman correlation."""
    return stats.spearmanr(x, y)[0]


def pearson(x, y):
    """Compute Pearson correlation."""
    return stats.pearsonr(x, y)[0]


def similarity(left_vectors, right_vectors):
    """Compute cosine similarity between two matrices."""
    if left_vectors.shape != right_vectors.shape:
        raise Exception(
            'Cannot compute similarity from numpy arrays of different shape: '
            '{} != {}'.format(left_vectors.shape(), right_vectors.shape()))
    dotprod = np.einsum('ij,ij->i', left_vectors, right_vectors)
    norms = np.linalg.norm(left_vectors, axis=1) * np.linalg.norm(
        right_vectors, axis=1)
    return dotprod / norms


def energy(matrix):
    """Compute the energy of the model.

    Energy is defined as the square of the Frobenius norm, which is also
    the square sum of singular values.
    """
    if matrix.ndim == 1:
        logger.info('Computing energy from singular values...')
        return np.sum(matrix**2)
    if matrix.__class__.__name__ != 'csr_matrix':
        raise Exception('Cannot compute energy on non-CSR sparse matrix')
    logger.info('Computing energy from squared Frobenius norm of scipy '
                'csr_matrix...')
    return matrix.power(2).sum()
