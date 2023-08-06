__all__ = ['norm_weights_from_pseudo_weights', \
			'postprocess', 'get_pseudo_weights', 'get_norm_weights', 'get_balanced_classifier_outputs', 'get_aggregate_classifier_output', \
			'get_neg_ctc_cost', 'get_unnorm_neg_ctc_cost']

import tensorflow as _tf
from . import _gen_utils

def get_balanced_single_classifier_output(y_pred_variate, pseudo_weights_variate, weights):
	# y_pred_variate indices: batch, component
	# pseudo_weights_variate indices: component
	# weights: component
	
	y_pred_variate = _tf.convert_to_tensor(y_pred_variate)
	pseudo_weights_variate = _tf.cast(_tf.convert_to_tensor(pseudo_weights_variate), dtype=y_pred_variate.dtype)
	weights = _tf.cast(_tf.convert_to_tensor(weights), dtype=y_pred_variate.dtype)
	
	ans = (y_pred_variate*weights)/pseudo_weights_variate # indices: batch, component
	ans /= _tf.reduce_sum(ans, axis=1, keepdims=True)
	
	return _gen_utils.tensor_to_numpy(ans)

# Computed using _pseudo_weights_postprocess_tf_backend ############################################

def norm_weights_from_pseudo_weights(pseudo_weights):
	# pseudo_weights indices: variate, component ###########
	return _gen_utils.tensor_to_numpy( _pseudo_weights_postprocess_tf_backend(pseudo_weights, mode='norm_weights') )

def _pseudo_weights_postprocess_tf_backend(pseudo_weights, mode):
	# pseudo_weights indices: variate, component ###########
	pseudo_weights = _tf.convert_to_tensor(pseudo_weights)
	unnorm_weights = _tf.math.exp(_tf.math.reduce_mean(_tf.math.log(pseudo_weights), axis=0))
	
	if mode == 'norm_weights':
		return unnorm_weights / _tf.math.reduce_sum(unnorm_weights, axis=0)
####################################################################################################

# Computed using _inclass_tf_backend ###############################################################

def postprocess(y_pred, sample_weight=None, pseudo_weights=None):
	# y_pred indices: batch, variate, component ############
	# pseudo_weights indices: variate, component ###########
	return_dict = _inclass_tf_backend(y_pred, sample_weight, mode='postprocess', pseudo_weights=pseudo_weights)
	for key in return_dict:
		return_dict[key] = _gen_utils.tensor_to_numpy(return_dict[key])
	
	return return_dict

def get_pseudo_weights(y_pred, sample_weight=None):
	# y_pred indices: batch, variate, component ############
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='pseudo_weights') )

def get_norm_weights(y_pred, sample_weight=None):
	# y_pred indices: batch, variate, component ############
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='norm_weights') )

def get_balanced_classifier_outputs(y_pred, sample_weight=None, pseudo_weights=None):
	# y_pred indices: batch, variate, component ############
	# pseudo_weights indices: variate, component ###########
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='balanced_classifier_outputs', pseudo_weights=pseudo_weights) )

def get_aggregate_classifier_output(y_pred, sample_weight=None, pseudo_weights=None):
	# y_pred indices: batch, variate, component ############
	# pseudo_weights indices: variate, component ###########
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='aggregate_classifier_output', pseudo_weights=pseudo_weights) )

def get_neg_ctc_cost(y_pred, sample_weight=None, pseudo_weights=None):
	# y_pred indices: batch, variate, component ############
	# pseudo_weights indices: variate, component ###########
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='neg_ctc_cost', pseudo_weights=pseudo_weights) )

def get_unnorm_neg_ctc_cost(y_pred, sample_weight=None, pseudo_weights=None):
	# y_pred indices: batch, variate, component ############
	# pseudo_weights indices: variate, component ###########
	return _gen_utils.tensor_to_numpy( _inclass_tf_backend(y_pred, sample_weight, mode='unnorm_neg_ctc_cost', pseudo_weights=pseudo_weights) )	

def _inclass_tf_backend(y_pred, sample_weight, mode, pseudo_weights=None):
	epsilon = 1e-9
	
	# y_pred indices: batch, variate, component ############
	y_pred = _tf.convert_to_tensor(y_pred)
	########################################################
	
	# Normalized sample_weight (indices: batch) ############
	if sample_weight is None:
		sample_weight = _tf.ones(shape=y_pred.shape[0], dtype=y_pred.dtype)
	else:
		sample_weight = _tf.cast(_tf.convert_to_tensor(sample_weight), dtype=y_pred.dtype)
		sample_weight = _tf.math.divide(sample_weight, _tf.math.reduce_mean(sample_weight))
	########################################################
	
	num_variates = y_pred.shape[1]
	num_components = y_pred.shape[2] #not needed
	
	if pseudo_weights is None:
		pseudo_weights = _tf.math.reduce_mean(y_pred * _tf.reshape(sample_weight, (-1, 1, 1)), axis=0) # indices: variate, component
		
		# Clip small weights and renormalize ###############
		pseudo_weights = _gen_utils.clip_by_value_keep_gradient(pseudo_weights, epsilon, 1.)
		pseudo_weights = pseudo_weights / _tf.math.reduce_sum(pseudo_weights, axis=1, keepdims=True)
		####################################################
	else:
		pseudo_weights = _tf.cast(_tf.convert_to_tensor(pseudo_weights), dtype=y_pred.dtype)
	
	if mode == 'pseudo_weights':
		return pseudo_weights
		
	# Geometric mean #######################################
	unnorm_weights = _tf.math.exp(_tf.math.reduce_mean(_tf.math.log(pseudo_weights), axis=0)) # indices: component
	########################################################
	
	if mode == 'norm_weights':
		return unnorm_weights / _tf.math.reduce_sum(unnorm_weights, axis=0)
	
	if mode == 'balanced_classifier_outputs':
		tmp = (y_pred * unnorm_weights) / pseudo_weights # indices: batch, variate, component
		return tmp / _tf.math.reduce_sum(tmp, axis=2, keepdims=True)
	
	# Unnormalized aggregate classifier ####################
	unnorm_aggregate_classifier = _tf.math.reduce_prod(y_pred, axis=1) * _tf.math.pow(unnorm_weights, 1-num_variates) # indices: batch, component
	########################################################
	
	if mode == 'aggregate_classifier_output':
		return unnorm_aggregate_classifier / _tf.math.reduce_sum(unnorm_aggregate_classifier, axis=1, keepdims=True)
	
	# Unnormalized ctc #####################################
	unnorm_ctc = _tf.math.reduce_mean(_tf.math.log(_tf.math.reduce_sum(unnorm_aggregate_classifier, axis=1)) * sample_weight, axis=0)
	########################################################
	
	if mode == 'unnorm_neg_ctc_cost':
		return -unnorm_ctc
	
	# ctc normalization factor #############################
	ctc_norm = _tf.math.log(_tf.math.reduce_sum(unnorm_weights, axis=0)) # indices: None
	########################################################
	
	if mode == 'neg_ctc_cost':
		return ctc_norm - unnorm_ctc
		
	if mode == 'postprocess':
		tmp = (y_pred * unnorm_weights) / pseudo_weights
		return {'pseudo_weights': pseudo_weights, \
				'norm_weights': unnorm_weights / _tf.math.reduce_sum(unnorm_weights, axis=0), \
				'balanced_classifier_outputs': tmp / _tf.math.reduce_sum(tmp, axis=2, keepdims=True), \
				'aggregate_classifier_output': unnorm_aggregate_classifier / _tf.math.reduce_sum(unnorm_aggregate_classifier, axis=1, keepdims=True), \
				'unnorm_neg_ctc_cost': -unnorm_ctc, \
				'neg_ctc_cost': ctc_norm - unnorm_ctc }
####################################################################################################
