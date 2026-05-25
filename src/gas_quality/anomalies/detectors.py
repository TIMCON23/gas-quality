import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


def isolation_forest_score(X):
    clf = IsolationForest(contamination=0.15, random_state=42)
    clf.fit(X)
    scores = -clf.decision_function(X)
    preds = (clf.predict(X) == -1).astype(int)
    return scores, preds


def dbscan_score(X, eps=0.6, min_samples=8):
    clusters = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
    preds = (clusters == -1).astype(int)
    return preds.astype(float), preds


def autoencoder_score(X):
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    ae = MLPRegressor(hidden_layer_sizes=(16, 8, 16), max_iter=400, random_state=42)
    ae.fit(Xs, Xs.ravel())
    recon = ae.predict(Xs)
    err = np.abs(Xs.ravel() - recon)
    return err, (err > np.percentile(err, 85)).astype(int)
