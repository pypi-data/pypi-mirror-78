## function for ensembling using K-Fold Training (Data Enembling) & obtaining predictions
def k_fold_train_cv(k, tpu, n_class, model_name, train_tfrecs_path, val_tfrecs_path, GCS_DS_PATH, BATCH_SIZE, EPOCHS, classification_model = 'default', freeze = False, input_shape = [512,512,3], activation = 'softmax', weights = "imagenet", optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = "sparse_categorical_accuracy", callbacks = None, plot = False):

	kfolds = KFold(k, shuffle = True, random_state = 21)

	TRAINING_FILENAMES = tf.io.gfile.glob(GCS_DS_PATH + train_tfrecs_path) + tf.io.gfile.glob(GCS_DS_PATH + val_tfrecs_path)

	from quick_ml.load_models_quick import create_model
	from quick_ml.begin_tpu import load_dataset

	df = pd.DataFrame(columns = ['Model_Fold_Number', 'Accuracy_top1', 'Accuracy_top3', "Val_Accuracy_top1", "Val_Accuracy_top3"])

	for fold, (trn_ind, val_ind) in enumerate(kfolds.split(TRAINING_FILENAMES)):
			
		train_dataset = load_dataset(list(pd.DataFrame({'TRAINING_FILENAMES' : TRAINING_FILENAMES}).loc[trn_ind]['TRAINING_FILENAMES']), labeled = True)
		val_dataset = load_dataset(list(pd.DataFrame({'TRAINING_FILENAMES' : TRAINING_FILENAMES}).loc[val_ind]['TRAINING_FILENAMES']), labeled = True, ordered = True)

		STEPS_PER_EPOCH = len(list(train_dataset)) // BATCH_SIZE

		train_dataset = train_dataset.repeat()
		train_dataset = train_dataset.shuffle(2048)
		train_dataset = train_dataset.batch(BATCH_SIZE)
		train_dataset = train_dataset.prefetch(tf.data.experimental.AUTOTUNE)

		val_dataset = val_dataset.batch(BATCH_SIZE)
		val_dataset = val_dataset.cache()
		val_dataset = val_dataset.prefetch(tf.data.experimental.AUTOTUNE)

		
		tf.tpu.experimental.initialize_tpu_system(tpu)
		strategy = tf.distribute.experimental.TPUStrategy(tpu)
		with strategy.scope():
			if classification_model != 'default':
				model = create_model(freeze = freeze, input_shape = input_shape, activation = activation, weights = weights, optimizer = optimizer, loss =loss, metrics = metrics, classes = n_class, model_name = model_name, classification_model = classification_model)
			else:
				model = create_model(freeze = freeze, input_shape = input_shape, activation = activation, weights = weights, optimizer = optimizer, loss = loss, metrics = metrics, classes = n_class, model_name = model_name)


		history = model.fit(train_dataset, epochs = EPOCHS, steps_per_epoch = STEPS_PER_EPOCH, validation_data = val_dataset)

		tf.keras.backend.clear_session()
		tf.compat.v1.reset_default_graph()
		del model 
		gc.collect()

		df = df.append(pd.DataFrame([[model_name + f'_fold_{fold}', history.history[metrics][-1], np.mean(history.history[metrics][-3:]) , history.history['val_' + metrics][-1], np.mean(history.history['val_' + metrics][-3:])]], columns = ['Model_Fold_Number', 'Accuracy_top1', 'Accuracy_top3', "Val_Accuracy_top1", "Val_Accuracy_top3"]), ignore_index = True)
		print(f"Done with the model fold -> {model_name}_fold_{fold}")

	return df


if __name__ != '__main__':
	import numpy as np
	import pandas as pd
	from sklearn.model_selection import KFold
	import os
	import tensorflow as tf
	if tf.__version__ != '2.2.0':
		raise Exception("Error! Tensorflow version mismatch!...")
	