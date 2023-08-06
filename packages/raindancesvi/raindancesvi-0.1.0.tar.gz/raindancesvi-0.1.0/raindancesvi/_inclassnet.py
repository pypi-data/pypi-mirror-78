__all__ = ['InClassNet']

import numpy as _np
import tensorflow as _tf
import inspect as _inspect
import functools as _functools
from . import _gen_utils

def _model_enable_dummy_target(cls):
	def func_enable_dummy_target(func):
		@_functools.wraps(func)
		def modified_func(*args, **kwargs):
			improper_dummy_target_message = "The argument `y` is allowed to be 'dummy' only if `x` is a non-empty list (or dict) of numpy arrays (with ndim > 0)."
			orig_signature = _inspect.signature(func)
			bound_args = orig_signature.bind(*args, **kwargs)
			
			
			if isinstance(bound_args.arguments['y'], str) and bound_args.arguments['y'] == 'dummy':
				x = bound_args.arguments['x']
				if isinstance(x, list) and len(x) > 0:
					inner_x = x[0]
				elif isinstance(x, dict) and len(x) > 0:
					inner_x = next(iter(x.values()))
				else:
					raise ValueError(improper_dummy_target_message)
				
				if isinstance(inner_x, _np.ndarray) and inner_x.ndim > 0:
					bound_args.arguments['y'] = _np.zeros(len(inner_x))
				else:
					raise ValueError(improper_dummy_target_message)
			
			return func(*bound_args.args, **bound_args.kwargs)
		
		return modified_func
	
	for func_name in ['evaluate', 'fit', 'test_on_batch', 'train_on_batch']:
		if hasattr(cls, func_name): #In case tensorflow removes one of these methods
			setattr(cls, func_name, func_enable_dummy_target(getattr(cls, func_name)))
			
			docstring_update = f"""This method is a wrapper around tensorflow.keras.Model.{func_name}.
The only modification is that `y` can be set to the string value 'dummy'.

Setting y = 'dummy':
 * Passes along a dummy target to the original `{func_name}` method.
 * Is only supported if `x` is a non-empty list (or dict) of numpy arrays.
   The arrays should not be numpy scalars (ndim should be > 0)."""
			
			tmp = getattr(cls, func_name)
			
			if tmp.__doc__ is None:
				tmp.__doc__ = docstring_update
			else:
				tmp.__doc__ = docstring_update + f"\n\nOriginal docstring of tensorflow.keras.Model.{func_name}:\n\n" + tmp.__doc__
	
	return cls

@_model_enable_dummy_target
class InClassNet(_tf.keras.Model):
	def __init__(self, classifiers, model_name=None, merged_output_names=None):
		# Begin input processing ##########################################
		
		##########################################
		# `classifiers` should be a list
		try:
			assert isinstance(classifiers, list)
			assert len(classifiers) > 1
		except AssertionError:
			raise ValueError("The argument `classifiers` should be a list of (at least 2) models.")
		##########################################
		
		##########################################
		# Each classifier should be a Model
		try:
			for classifier in classifiers:		
				assert isinstance(classifier, _tf.keras.Model)
		except AssertionError:
			raise TypeError("The argument `classifiers` should be list of objects of type `tensorflow.keras.Model`.")
		##########################################
		
		##########################################
		# classifiers can have multiple (but equal number of) outputs
		self._inclass_outputs_len = len(classifiers[0].outputs)
		try:
			for classifier in classifiers:
				assert len(classifier.outputs) == self._inclass_outputs_len
		except AssertionError:
			raise ValueError("The classifier models in `classifiers` should return the same number of outputs.")
		##########################################
		
		##########################################
		# The different outputs can have different number of categories
		# But they should match across different classifiers
		self._inclass_output_shapes_list = classifiers[0].output_shape
		if not isinstance(self._inclass_output_shapes_list, list):
			self._inclass_output_shapes_list = [self._inclass_output_shapes_list]
		
		try:
			for classifier in classifiers:
				tmp = classifier.output_shape
				if not isinstance(tmp, list):
					tmp = [tmp]
				assert tmp == self._inclass_output_shapes_list
		except:
			raise ValueError("The shapes of the outputs of all the classifiers should match. If each classifier returns multiple outputs, the shapes of the i-th outputs of all the classifiers should match, but can differ for different i-s.")
		##########################################
		
		if merged_output_names is None:
			merged_output_names_list = [None]*self._inclass_outputs_len
		elif isinstance(merged_output_names, list):
			merged_output_names_list = merged_output_names
		else:
			merged_output_names_list = [merged_output_names]
		
		# End input processing ############################################
		
		self._inclass_num_variates = len(classifiers)
		self._inclass_num_components = [self._inclass_output_shapes_list[i][1] for i in range(self._inclass_outputs_len)]
		
		# Combining inputs and outputs ###########
		merged_inputs = []
		for classifier in classifiers:
			merged_inputs.extend(classifier.inputs)
		
		merged_outputs = []
		for i in range(self._inclass_outputs_len):
			if merged_output_names_list[i] is None:
				kwargs = {}
			else:
				kwargs = {'name': merged_output_names_list[i]}
			
			merged_outputs.append( _gen_utils.StackLayer(axis=0, **kwargs) ([classifier.outputs[i] for classifier in classifiers]) )
		##########################################
		
		super().__init__(inputs = merged_inputs, outputs = merged_outputs, name=model_name)
