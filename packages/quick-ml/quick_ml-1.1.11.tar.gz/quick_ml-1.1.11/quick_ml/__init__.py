import tensorflow as tf
if tf.__version__ == '2.2.0':
	print(f"Tensorflow imported successfully. Tensorflow version -> {tf.__version__}")
else:
	print("Tensorflow version mismatch!. Please check tensorflow isn't imported before installing quick_ml. Restart the session to fix the error.")

from quick_ml import tfrecords_maker
from quick_ml import begin_tpu
from quick_ml import visualize_and_check_data
from quick_ml import load_models_quick
from quick_ml import training_predictions
from quick_ml import predictions
from quick_ml import augments

__version__ = '1.1.11'
