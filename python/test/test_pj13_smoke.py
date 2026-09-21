import numpy as np

import magic


def test_import_and_fit_transform_shape():
    rng = np.random.RandomState(0)
    X = rng.poisson(1.0, size=(200, 60)).astype(float)
    op = magic.MAGIC(knn=5, n_pca=20, t=3, random_state=0, verbose=0)
    Y = op.fit_transform(X, genes="all_genes")
    assert np.asarray(Y).shape == X.shape
