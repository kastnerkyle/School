#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from itertools import cycle
from sklearn.utils import check_random_state
from sklearn.metrics.pairwise import euclidean_distances

class FuzzyKMeans(KMeans):
    def __init__(self, k, m=2, max_iter=100, random_state=0, tol=1e-4):
        """
        m > 1: fuzzy-ness parameter
        The closer to m is to 1, the closter to hard kmeans.
        The bigger m, the fuzzier (converge to the global cluster).
        """
        self.k = k
        assert m > 1
        self.m = m
        self.max_iter = max_iter
        self.random_state = random_state
        self.tol = tol

    def _e_step(self, X):
        D = 1.0 / euclidean_distances(X, self.cluster_centers_, squared=True)
        D **= 1.0 / (self.m - 1)
        D /= np.sum(D, axis=1)[:, np.newaxis]
        # shape: n_samples x k
        self.fuzzy_labels_ = D
        self.labels_ = self.fuzzy_labels_.argmax(axis=1)

    def _m_step(self, X):
        weights = self.fuzzy_labels_ ** self.m
        # shape: n_clusters x n_features
        self.cluster_centers_ = np.dot(X.T, weights).T
        self.cluster_centers_ /= weights.sum(axis=0)[:, np.newaxis]

    def fit(self, X, y=None):
        n_samples, n_features = X.shape
        vdata = np.mean(np.var(X, 0))

        random_state = check_random_state(self.random_state)
        self.fuzzy_labels_ = random_state.rand(n_samples, self.k)
        self.fuzzy_labels_ /= self.fuzzy_labels_.sum(axis=1)[:, np.newaxis]
        self._m_step(X)

        for i in xrange(self.max_iter):
            centers_old = self.cluster_centers_.copy()

            self._e_step(X)
            self._m_step(X)

            if np.sum((centers_old - self.cluster_centers_) ** 2) < self.tol * vdata:
                break

        return self

if __name__ == "__main__":
    digits = load_digits()
    X = scale(digits.data)
    y = digits.target
    pca = PCA(n_components=2)
    pca.fit(X)
    reduced = pca.transform(X)
    km = KMeans(n_clusters=10)
    km.fit(reduced)
    km_cent = km.cluster_centers_
    fcm = FuzzyKMeans(k=10, m=3)
    fcm.fit(reduced)
    fcm_cent = fcm.cluster_centers_
    colors = cycle('bgrcmyk')
    for t, col in zip(set(y), colors):
        plt.scatter(reduced[y == t, 0], reduced[y == t, 1],
                    c=col, marker='o', label=str(t), alpha=.2)
    plt.scatter(km_cent[:, 0], km_cent[:, 1], c="darkred", s=50,
                marker='o', label="kmeans")
    plt.scatter(fcm_cent[:, 0], fcm_cent[:, 1], c="darkblue", s=50,
                marker='o', label="fuzzy")
    plt.title("Clustered Digits")
    plt.legend()
    plt.show()
