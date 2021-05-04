# model=['ovr_svm']

from sklearn.svm import SVC
from ..AL_query.alipy_rank.index.index_collections import MultiLabelIndexCollection
import numpy as np
import copy


def _check_multi_label_ind(container, label_mat_shape, order='F'):
    """Check if the given array is an array of multi label indexes.

    Parameters
    ----------
    container: object
        index object.

    label_mat_shape: tuple
        The shape of label matrix. (row, col)

    order: {'C', 'F'}
        ONLY USEFUL when a 1d array is given.
        Determines whether the indices should be viewed as indexing in
        row-major (C-style) or column-major (Matlab-style) order.

    """
    if not isinstance(container, MultiLabelIndexCollection):
        try:
            if isinstance(container[0], tuple):
                container = MultiLabelIndexCollection(container, label_mat_shape[1])
            else:
                container = MultiLabelIndexCollection.construct_by_1d_array(container, label_mat_shape=label_mat_shape, order='F')
        except:
            raise ValueError(
                "Please pass a 1d array of indexes or MultiLabelIndexCollection (column major, "
                "start from 0) or a list "
                "of tuples with 2 elements, in which, the 1st element is the index of instance "
                "and the 2nd element is the index of label.")
    return copy.copy(container)


class OVRModel:
    '''Train a list of model for multi label setting.'''

    def __init__(self, model=None):
        self.base_model = model
        self.models = None

    def fit(self, X, y, matrix_type='labeled', labeled_index=None):
        """Train a list of model for multi label setting.

        :param X: 2D array
            Feature matrix.

        :param y: 2D array
            Multi label target.

        :param matrix_type: {'labeled', 'full'} (optional, default='labeled')
            The matrix X and y is the labeled part or the full data matrix.
            'labeled': The X and y is fully labeled.
            'full': Some entries of X and y are treated as unknown. Use labeled_index
            to specify the known entries.

        :param labeled_index: {list, np.ndarray, MultiLabelIndexCollection}
            The indexes of labeled samples. It should be a 1d array of indexes (column major, start from 0) or
            MultiLabelIndexCollection or a list of tuples with 2 elements, in which,
            the 1st element is the index of instance and the 2nd element is the index of labels.
        """
        X = np.asarray(X)
        y = np.asarray(y)
        if self.base_model is None:
            basemodel = SVC()
        else:
            basemodel = self.base_model
        if matrix_type == 'labeled':
            self.models = []
            for j in np.arange(y.shape[1]):
                m = copy.deepcopy(basemodel)
                m.fit(X, y[:, j])
                self.models.append(m)
        elif matrix_type == 'full':
            labeled_index = _check_multi_label_ind(labeled_index, y.shape)
            train_traget = labeled_index.get_matrix_mask(y.shape, sparse=False)
            self.models = []
            for j in np.arange(y.shape[1]):
                j_target = train_traget[:, j]
                i_samples = np.where(j_target!=0)[0]
                m = copy.deepcopy(basemodel)
                m.fit(X[i_samples, :], y[i_samples, j])
                self.models.append(m)
        else:
            raise ValueError("matrix_type must be one of {'labeled', 'full'}")

    def predict(self, X):
        if not self.models:
            raise ValueError("Predict before training.")
        return np.argmax([m.predict(X) for m in self.models], axis=0)

    def decision_function(self, X):
        if not self.models:
            raise ValueError("Predict before training.")
        return np.asarray([m.predict(X) for m in self.models]).T
