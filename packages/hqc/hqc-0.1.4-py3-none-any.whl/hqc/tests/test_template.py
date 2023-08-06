import pytest
import numpy as np

from sklearn.datasets import load_iris
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_allclose

from hqc import HQC


@pytest.fixture
def data():
    return load_iris(return_X_y=True)

def test_template_classifier(data):
    X, y = data
    clf = HQC()
    assert clf.rescale == 1
    assert clf.encoding == 'amplit'
    assert clf.n_copies == 1
    assert clf.class_wgt == 'equi'
    assert clf.n_jobs == 1
    assert clf.n_splits == 1

    clf.fit(X, y)
    assert hasattr(clf, 'classes_')
#     assert hasattr(clf, 'X_')
#     assert hasattr(clf, 'y_')

    y_pred = clf.predict(X)
    assert y_pred.shape == (X.shape[0],)
