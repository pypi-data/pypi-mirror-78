"""Dataset utils."""
import os
import logging
import csv

from collections import defaultdict


__all__ = ('load_dataset', 'load_dataset_words')


logger = logging.getLogger(__name__)

DATASETS = {
    'ap': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       'resources', 'ap.csv'),
    'battig': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           'resources', 'battig.csv'),
    'essli': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'resources', 'essli-2008.csv'),
    'men': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'resources', 'MEN_dataset_natural_form_full'),
    'simlex': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                           'resources', 'SimLex-999.txt'),
    'simverb': os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'resources', 'SimVerb-3500.txt'),
}


def _load_categories_to_words_dict(dataset, vocab):
    if dataset not in ['ap', 'battig', 'essli']:
        raise Exception('Invalid concept categorization dataset: {}'
                        .format(dataset))
    categories_to_words = defaultdict(list)
    total_num_rows = 0
    with open(DATASETS[dataset], newline='') as csv_stream:
        next(csv_stream)
        reader = csv.reader(csv_stream, quotechar='|')
        for row in reader:
            if row[2]:
                total_num_rows += 1
                if row[2] in vocab:
                    categories_to_words[row[1]].append(row[2])
                else:
                    logger.info('Word not in vocabulary: {}'.format(row[2]))
    logger.info('Processing {} words out of {} in {} categories'
                .format(sum(len(x) for x in categories_to_words.values()),
                        total_num_rows, len(categories_to_words)))
    return categories_to_words


# pylint: disable=C0103
def _load_idx_and_sim(left, right, sim, vocab, dataset):
    """Load discretized features and similarities for a given dataset.

    Will retain only words that are in the vocabulary.
    Will filter sim accordingly. Will normalize sim between [0, 1]
    """
    left_idx = []
    right_idx = []
    f_sim = []
    if dataset not in ['men', 'simlex', 'simverb']:
        raise Exception('Unsupported dataset {}'.format(dataset))
    for l, r, s in zip(left, right, sim):
        # if l not in vocab:
        #     raise Exception('Word {} not in {} dataset'
        #                     .format(l, dataset))
        # if r not in vocab:
        #     raise Exception('Word {} not in {} dataset'
        #                     .format(r, dataset))
        if l in vocab and r in vocab:
            left_idx.append(vocab[l])
            right_idx.append(vocab[r])
            if dataset == 'men':  # men has sim in [0, 50]
                f_sim.append(s/50)
            else:  # all other datasets have sim in [0, 10]
                f_sim.append(s/10)
    logger.info('Testing on {} pairs out of {}'
                .format(len(f_sim), len(sim)))
    ratio = (len(f_sim) / len(sim)) * 100
    logger.info('Test pairs ratio = {}%'.format(round(ratio, 2)))
    return left_idx, right_idx, f_sim


def _load_word_pairs_and_sim(dataset):
    """Load word pairs and similarity from a given dataset."""
    if dataset not in ['men', 'simlex', 'simverb']:
        raise Exception('Unsupported dataset {}'.format(dataset))
    left = []
    right = []
    sim = []
    with open(DATASETS[dataset], 'r', encoding='utf-8') as data_stream:
        for line in data_stream:
            line = line.rstrip('\n')
            items = line.split()
            left.append(items[0])
            right.append(items[1])
            if dataset == 'men':
                sim.append(float(items[2]))
            else:
                sim.append(float(items[3]))
    return left, right, sim


def load_dataset(dataset, vocab):
    """Load dataset for concept categorization or word similarity."""
    if dataset not in ['ap', 'battig', 'essli', 'men', 'simlex', 'simverb']:
        raise Exception('Unsupported dataset: {}'.format(dataset))
    if dataset in ['men', 'simlex', 'simverb', 'ws353']:
        left, right, sim = _load_word_pairs_and_sim(dataset)
        return _load_idx_and_sim(left, right, sim, vocab, dataset)
    return _load_categories_to_words_dict(dataset, vocab)


def load_dataset_words(dataset):
    """Load set of words found in dataset."""
    if dataset not in ['men', 'simlex', 'simverb']:
        raise Exception('Unsupported dataset: {}'.format(dataset))
    words = set()
    with open(DATASETS[dataset], 'r', encoding='utf-8') as data_stream:
        for line in data_stream:
            line = line.rstrip('\n')
            items = line.split()
            words.add(items[0])
            words.add(items[1])
    return words
