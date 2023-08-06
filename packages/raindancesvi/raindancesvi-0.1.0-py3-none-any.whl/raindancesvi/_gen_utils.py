import tensorflow as _tf

@_tf.custom_gradient
def clip_by_value_keep_gradient(x, clip_value_min, clip_value_max):
	y = _tf.clip_by_value(x, clip_value_min, clip_value_max)
	def grad(dy):
		return dy, dy*0., dy*0.
	return y, grad

def tensor_to_numpy(x, ignore_nontensor=False):
	if _tf.is_tensor(x):
		if hasattr(x, 'numpy'):
			try:
				return x.numpy()
			except:
				pass
		elif hasattr(x, 'eval'):
			try:
				return x.eval(session=_tf.compat.v1.Session())
			except:
				pass
		raise RuntimeError("Unable to convert tensor to numpy array.")
	elif ignore_nontensor:
		return x
	else:
		raise TypeError("tensor_to_numpy function expects a tensor input. Set 'ignore_nontensor' argument to True to ignore this error message.")

class StackLayer(_tf.keras.layers.Lambda):
	def __init__(self, axis=0, name=None):
		batch_adjusted_axis = axis
		if axis >= 0:
			batch_adjusted_axis += 1
		
		super().__init__(_tf.stack, arguments={'axis': batch_adjusted_axis}, name=name)
