"""Evaluate embeddings on various tasks."""
import logging

import numpy as np
from sklearn.cluster import KMeans

import embeddix.utils.files as futils
import embeddix.utils.metrix as metrix
import embeddix.utils.data as dutils

__all__ = ('evaluate_distributional_space', 'evaluate_word_similarity')

logger = logging.getLogger(__name__)


def _evaluate_concept_categorization(model, vocab, dataset):
    if dataset not in ['ap', 'battig', 'essli']:
        raise Exception('Invalid concept categorization dataset: {}'
                        .format(dataset))
    logger.info('Evaluating concept categorization on {}'.format(dataset))
    categories_to_words = dutils.load_dataset(dataset, vocab)
    categories = categories_to_words.keys()
    centroids = np.empty(shape=(len(categories), model.shape[1]))
    for idx, (_, words) in enumerate(categories_to_words.items()):
        word_idxx = [vocab[word] for word in words]
        centroids[idx] = np.mean(model[word_idxx, :], axis=0)
    category_words = [word for words in categories_to_words.values()
                      for word in words]
    category_words_idx = [vocab[word] for word in category_words]
    pred_clusters = KMeans(init=centroids, n_init=1,
                           n_clusters=len(categories)).fit_predict(
                               model[category_words_idx, :])
    true_clusters = np.array([idx for idx, words in
                              enumerate(categories_to_words.values())
                              for _ in words])
    purity = metrix.purity(true_clusters, pred_clusters)
    logger.info('Cluster purity = {}'.format(purity))
    return purity


def evaluate_word_similarity(model, vocab, dataset):
    """Evaluate lexical similarity/relatedness."""
    if dataset not in ['men', 'simlex', 'simverb']:
        raise Exception('Invalid similarity dataset: {}'.format(dataset))
    logger.info('Evaluating word similarity on {}'.format(dataset))
    left_idx, right_idx, sim = dutils.load_dataset(dataset, vocab)
    left_vectors = model[left_idx]
    right_vectors = model[right_idx]
    model_sim = metrix.similarity(left_vectors, right_vectors)
    spr = metrix.spearman(sim, model_sim)
    logger.info('Spearman correlation = {}'.format(spr))
    return spr


def evaluate_distributional_space(embeddings_filepath, vocab_filepath,
                                  dataset):
    """Evaluate embeddings on lexical similarity or concept categorization."""
    if dataset not in ['ap', 'battig', 'essli', 'men', 'simlex', 'simverb']:
        raise Exception('Unsupported dataset: {}'.format(dataset))
    model = np.load(embeddings_filepath)
    vocab = futils.load_vocab(vocab_filepath)
    if dataset in ['men', 'simlex', 'simverb']:
        return evaluate_word_similarity(model, vocab, dataset)
    return _evaluate_concept_categorization(model, vocab, dataset)
