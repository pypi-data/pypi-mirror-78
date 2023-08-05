def _int64_feature(value):
	return tf.train.Feature(int64_list = tf.train.Int64List(value = [value]))

def _bytes_feature(value):
	return tf.train.Feature(bytes_list = tf.train.BytesList(value = [value]))

def load_image(addr, IMAGE_SIZE = (192,192)):
	# read the img & resize to the image size
	# converting the loaded BGR image to RGB image

	img = cv2.imread(addr)
	if img is None:
		return None
	img = cv2.resize(img, IMAGE_SIZE, interpolation = cv2.INTER_CUBIC)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	return img

def get_addrs_labels(data_dir):

	data_path = data_dir + '/*/*.jpg'

	addrs = glob.glob(data_path)
	
	classes = os.listdir(data_dir)
	classes.sort()

	labels_dict = {}
	for i, class_ in enumerate(classes):
		labels_dict[class_] = i
	print(f"Class Encodings for the Dataset Folder is as follows -> \n\n {labels_dict}")
	
	labels = []
	for addr in addrs:
		label = None
		for i in classes:
			if i in addr:
				label = i
				break
		labels.append(labels_dict[label])

	# shuffling the data
	c = list(zip(addrs, labels))
	shuffle(c)

	addrs, labels = zip(*c)

	return addrs, labels

def create_split_tfrecords_data(data_dir, outfile1name, outfile2name, split_size_ratio, IMAGE_SIZE = (192,192)):

	print(f"Split ratio -> {split_size_ratio}")
	addrs, labels = get_addrs_labels(data_dir)

	file1_addrs = addrs[0 : int(split_size_ratio * len(addrs))]
	file1_labels = labels[0: int(split_size_ratio * len(labels))]

	file2_addrs = addrs[int(split_size_ratio * len(addrs)) :]
	file2_labels =  labels[int(split_size_ratio * len(labels)):]

	create_tfrecord_labeled(file1_addrs, file1_labels, outfile1name, IMAGE_SIZE)
	create_tfrecord_labeled(file2_addrs, file2_labels, outfile2name, IMAGE_SIZE)

	print("Data Successfully created!")


def create_tfrecord_labeled(addrs, labels, out_filename, IMAGE_SIZE = (192,192)):


	print("""
		Ensure that the data directory has the following structure ->

		/data|
			 |
			 |-> class1
			 |-> class2
			 |-> class3
			 |-> class4
			 .
			 .
			 .
			 |-> classN

		the input to data_dir must the path to /data folder. & Make sure that the images are in .jpg format
		""")

	print(f"Beginning to write data to {out_filename}\n\n")
	writer = tf.io.TFRecordWriter(out_filename)
	for i in range(len(addrs)):
		if i % 300 == 0:
			print("Data written -> {}/{}".format(i, len(addrs)))
			sys.stdout.flush()

		# loading the image
		img = load_image(addrs[i], IMAGE_SIZE)
		label = labels[i]

		if img is None:
			continue

		# feature creation

		feature = {
			'image' : _bytes_feature(img.tostring()),
			'label' : _int64_feature(label)
		}

		

		# example protocol buffer
		example = tf.train.Example(features = tf.train.Features(feature = feature))

		# serialize the write the output to the file
		writer.write(example.SerializeToString())
	writer.close()
	sys.stdout.flush()
	print(f"Done with writing data to {out_filename}\n\n")
	print("""
			Your Labeled TFRecord Format is -> 

			{
			'image' : tf.io.FixedLenFeature([], tf.string),
			'label' : tf.io.FixedLenFeature([], tf.int64)
			}

			You would be asked the TFRecord Format while reading the training and validation dataset.
	""")
	print("Now after you have obtained the tfrecords, you need to upload them to GCS Buckets to utlize TPU computation...")
	print("To do so, the easiest method is uploading on Kaggle.")
	print("""
		1. Public Datasets

		from kaggle_datasets import KaggleDatasets
		GCS_DS_PATH = KaggleDatasets().get_gcs_path()


		2. Private Datasets

		# Get the credentials from the Cloud SDK
		from kaggle_secrets import UserSecretsClient
		user_secrets = UserSecretsClient()
		user_credential = user_secrets.get_gcloud_credential()

		# Set the credentials
		user_secrets.set_tensorflow_credential(user_credential)

		# Use a familiar call to get the GCS path of the dataset
		from kaggle_datasets import KaggleDatasets
		GCS_DS_PATH = KaggleDatasets().get_gcs_path()
		""")

def get_addrs_ids(data_dir):
	data_path = data_dir + '/*.jpg'

	addrs = glob.glob(data_path)

	ids = os.listdir(data_dir)


	return addrs, ids


def create_tfrecord_unlabeled(out_filename, addrs, ids, IMAGE_SIZE = (192,192)):
	print("""
		The Data for this should be unlabeled. 

		The folder structure should be

		data |
			 |
			 |->filename1.jpg
			 |->filename2.jpg
			 |->filename3.jpg
			 |->filename4.jpg
			 |.
			 ..
			 ..
			 |->filenameN.jpg


		""")

	print(f"Beginning to write the {out_filename}\n\n")
	writer = tf.io.TFRecordWriter(out_filename)
	for i in range(len(addrs)):
		if i % 300 == 0:
			print("Data Written -> {}/{}".format(i, len(addrs)))
			sys.stdout.flush()

		#loading the image
		img = load_image(addrs[i], IMAGE_SIZE)
		idnum = ids[i]

		if img is None:
			continue

		#feature creation
		feature = {
			'image' : _bytes_feature(img.tostring()),
			'idnum' : _bytes_feature(idnum.encode())
		}

		# example protocol buffer
		example = tf.train.Example(features = tf.train.Features(feature = feature))


		# serialize & write
		writer.write(example.SerializeToString())
	writer.close()
	sys.stdout.flush()

	print("""
			Your Unlabeled TFRecord Format is -> 

			{
			'image' : tf.io.FixedLenFeature([], tf.string),
			'idnum' : tf.io.FixedLenFeature([], tf.string)
			}

			You would be asked the TFRecord Format while reading the test dataset.
	""")
	print("After you have obtained the tfrecords, you need to upload the tfrecords to GCS Buckets for TPU computation")
	print("To do so, the easiest method is to upload on Kaggle. Either as a public or as a private dataset.")
	print("""
		NOTE: Fully Functional and working with Public Datasets
		1. Public Datasets

		from kaggle_datasets import KaggleDatasets
		GCS_DS_PATH = KaggleDatasets().get_gcs_path()


		NOTE : Not tested with Private Datasets
		2. Private Datasets

		# Get the credentials from the Cloud SDK
		from kaggle_secrets import UserSecretsClient
		user_secrets = UserSecretsClient()
		user_credential = user_secrets.get_gcloud_credential()

		# Set the credentials
		user_secrets.set_tensorflow_credential(user_credential)

		# Use a familiar call to get the GCS path of the dataset
		from kaggle_datasets import KaggleDatasets
		GCS_DS_PATH = KaggleDatasets().get_gcs_path()

		""")


if __name__ == "__main__":
	pass
else:
	import os
	import tensorflow as tf
	if tf.__version__ == '2.2.0':
		pass
	else:
		print("Tensorflow version Error!")
	from random import shuffle
	import glob
	import sys
	import cv2
	import numpy as np 