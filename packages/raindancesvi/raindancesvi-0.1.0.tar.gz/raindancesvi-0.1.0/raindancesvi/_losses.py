__all__ = ['neg_ctc_cost', 'unnorm_neg_ctc_cost']

from ._inclass_utils import _inclass_tf_backend

def neg_ctc_cost(y_true, y_pred, sample_weight=None):
	y_true = None # unsupervised
	return _inclass_tf_backend(y_pred, sample_weight, mode='neg_ctc_cost')

def unnorm_neg_ctc_cost(y_true, y_pred, sample_weight=None):
	y_true = None # unsupervised
	return _inclass_tf_backend(y_pred, sample_weight, mode='unnorm_neg_ctc_cost')
