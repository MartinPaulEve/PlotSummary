import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
import pkgutil
import re
from debug import Debug, Debuggable

import stemming.porter2
from nltk.stem import PorterStemmer
from sklearn.neighbors import KernelDensity
from collections import OrderedDict
from functools32 import lru_cache
from scipy.spatial import distance

class Text (Debuggable):


    @classmethod
    def from_file(cls, path, debug, stopwords=None, nostem=None):

        """
        Create a text from a file.

        Args:
            path (str): The file path.
        """

        with open(path, 'r') as f:
            return cls(f.read(), debug, stopwords, nostem)


    def __init__(self, text, debug, stopwords=None, nostem=None):

        """
        Store the raw text, tokenize.

        Args:
            text (str): The raw text string.
            stopwords (str): A custom stopwords list path.
        """

        self.debug = debug
        Debuggable.__init__(self, 'TextPlot')

        self.text = text
        self.load_stopwords(stopwords)
        self.load_nostem(nostem)
        self.tokenize()

    @staticmethod
    def show_stem(term):
        return stemming.porter2.stem(term)

    def stem(self, term):
        if not term in self.nostem:
            return stemming.porter2.stem(term)
        else:
            return term

    def load_nostem(self, path):

        """
        Load a set of words that should not be stemmed.

        Args:
            path (str): The stopwords file path.
        """

        if path:
            with open(path) as f:
                self.nostem = set(f.read().splitlines())

        else:
            self.nostem = []

    def load_stopwords(self, path):

        """
        Load a set of stopwords.

        Args:
            path (str): The stopwords file path.
        """

        if path:
            with open(path) as f:
                self.stopwords = set(f.read().splitlines())

        else:
            self.stopwords = set(
                pkgutil
                .get_data('textplot', 'data/stopwords.txt')
                .decode('utf8')
                .splitlines()
            )

    def tokenize(self):

        """
        Tokenize the text.
        """

        self.tokens = []
        self.terms = OrderedDict()

        # Generate tokens.
        for token in self.tokenizer(self.text):

            # Ignore stopwords.
            if token['unstemmed'] in self.stopwords:
                self.tokens.append(None)

            else:

                # Token:
                self.tokens.append(token)

                # Term:
                if token['unstemmed'] in self.nostem:
                    offsets = self.terms.setdefault(token['unstemmed'], [])
                else:
                    offsets = self.terms.setdefault(token['stemmed'], [])
                offsets.append(token['offset'])


    def tokenizer(self,text):

        """
        Yield tokens.

        Args:
            text (str): The original text.

        Yields:
            dict: The next token.
        """

        stem = PorterStemmer().stem
        tokens = re.finditer('[a-z]+', text.lower())

        for offset, match in enumerate(tokens):

            # Get the raw token.
            unstemmed = match.group(0)

            yield { # Emit the token.
                'stemmed':      stem(unstemmed),
                'unstemmed':    unstemmed,
                'offset':       offset
            }

    @lru_cache(maxsize=None)
    def kde(self, term, bandwidth=2000, samples=1000, kernel='gaussian'):

        """
        Estimate the kernel density of the instances of term in the text.

        Args:
            term (str): A stemmed term.
            bandwidth (int): The kernel bandwidth.
            samples (int): The number of evenly-spaced sample points.
            kernel (str): The kernel function.

        Returns:
            np.array: The density estimate.
        """

        # Get the offsets of the term instances.
        try:
            terms = np.array(self.terms[term])[:, np.newaxis]
        except:
            return 0

        # Fit the density estimator on the terms.
        kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(terms)

        # Score an evely-spaced array of samples.
        x_axis = np.linspace(0, len(self.tokens), samples)[:, np.newaxis]
        scores = kde.score_samples(x_axis)

        # Scale the scores to integrate to 1.
        return np.exp(scores) * (len(self.tokens) / samples)

    def plot_terms_raw_count(self, terms, caption, word_count):

        """
        Plot the X-axis offsets of a term.
        :param term: The unstemmed term to plot.
        """

        fig, ax = plt.subplots()

        # Be sure to only pick integer tick locations.
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_locator(ticker.MaxNLocator(integer=True))

        g1 = terms

        for term in g1:
            if self.stem(term) in self.terms:
                xs = self.terms[self.stem(term)]

                y,binEdges=np.histogram(xs, bins=len(self.tokens)/word_count, range=[0, len(self.tokens)])
                bincenters = 0.5*(binEdges[1:]+binEdges[:-1])

                average = int(float(sum(y))/float(len(y)))

                self.debug.print_debug(self, u'The term {0} appears on average {1} times every {2} words'.format(term, average, word_count))

                plt.plot(bincenters, y, label=term)

        plt.xlabel('Word Offset')
        plt.ylabel('Number of Occurrences')
        plt.title(caption)
        plt.legend(loc='upper right')

        fig = plt.gcf()
        fig.set_size_inches(10, 4)
        fig.tight_layout()

        return plt

    def plot_terms_histogram(self, terms, caption, word_count):

        """
        Plot the X-axis offsets of a term.
        :param term: The unstemmed term to plot.
        """

        fig, ax = plt.subplots()

        # Be sure to only pick integer tick locations.
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_locator(ticker.MaxNLocator(integer=True))

        g1 = terms

        for term in g1:
            if self.stem(term) in self.terms:
                xs = self.terms[self.stem(term)]
                plt.hist(xs, bins=len(self.tokens)/word_count, alpha=0.9, range=[0, len(self.tokens)], label=term)

        plt.xlim(0, len(self.tokens))
        plt.xlabel('Word Offset')
        plt.ylabel('Number of Occurrences')
        plt.title(caption)
        plt.legend(loc='upper right')

        fig = plt.gcf()
        fig.set_size_inches(10, 4)
        fig.tight_layout()

        return plt

    def plot_terms(self, terms, caption, **kwargs):
        g1 = terms

        for term in g1:
            kde = self.kde(self.stem(term), **kwargs)
            plt.plot(kde, label=term)

        plt.xlabel('Word Offset')
        plt.ylabel('Number of Occurrences')
        plt.title(caption)
        plt.legend(loc='upper right')

        fig = plt.gcf()
        fig.set_size_inches(10, 4)
        fig.tight_layout()

        return plt

    def plot_terms_two_groups(self, terms, term_name, second_terms, second_term_name, caption, **kwargs):

        """
        War vs. peace terms.
        """

        g1 = terms
        g2 = second_terms

        for term in g1:
            kde = self.kde(self.stem(term), **kwargs)
            plt.plot(kde, color='#e8a945', label=term_name)

        for term in g2:
            kde = self.kde(self.stem(term), **kwargs)
            plt.plot(kde, color='#0067a2', label=second_term_name)

        plt.xlabel('Word Offset')
        plt.ylabel('Number of Occurrences')
        plt.title(caption)

        w_patch = mpatches.Patch(color='#e8a945', label=term_name)
        p_patch = mpatches.Patch(color='#0067a2', label=second_term_name)
        plt.legend(handles=[w_patch, p_patch], loc='upper right')

        fig = plt.gcf()
        fig.set_size_inches(10, 4)
        fig.tight_layout()

        return plt

    def score_braycurtis(self, term1, term2, **kwargs):

        """
        Compute a weighting score based on the "City Block" distance between
        the kernel density estimates of two terms.
        :param term1: The first term.
        :param term2: The second term.
        """

        t1_kde = self.kde(term1, **kwargs)
        t2_kde = self.kde(term2, **kwargs)

        return 1-distance.braycurtis(t1_kde, t2_kde)

    def plot_kde_overlap(self, terms, color1='#0067a2', color2='#e8a945', overlap_color='#dddddd', **kwargs):

        term1 = terms[0]
        term2 = terms[1]

        t1 = self.stem(term1)
        t2 = self.stem(term2)

        bc = self.score_braycurtis(t1, t2, **kwargs)

        kde1 = self.kde(t1, **kwargs)
        kde2 = self.kde(t2, **kwargs)
        plt.plot(kde1, color=color1, label=term1)
        plt.plot(kde2, color=color2, label=term2)

        overlap = np.minimum(kde1, kde2)
        plt.fill(overlap, color=overlap_color)
        plt.title(term1+', '+term2+' - '+str(round(bc, 4)))

        plt.xlabel('Word Offset')
        plt.ylabel('Number of Occurrences')
        plt.legend(loc='upper right')

        fig = plt.gcf()
        fig.set_size_inches(10, 4)
        fig.tight_layout()

        return plt

    def sort_dict(self, d, reverse=True):

        """
        Sort an ordered dictionary by value, descending.
        :param d: A dictionary.
        """

        sort = sorted(d.iteritems(), key=lambda x: x[1], reverse=reverse)
        return OrderedDict(sort)

    def anchored_scores(self, anchor, method='braycurtis', **kwargs):

        """
        Compute the intersections between an anchor term and all other terms.
        :param anchor: The anchor term.
        :param method: The scoring function.
        """

        evaluator = getattr(self, 'score_'+method)

        pairs = OrderedDict()
        for term in self.terms:
            pairs[term] = evaluator(anchor, term, **kwargs)

        return self.sort_dict(pairs)

