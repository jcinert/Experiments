import os
import math
import numpy as np
import datetime as dt
from numpy import newaxis
from src.lstm.utils import Timer
from tensorflow.keras.layers import Dense, Activation, Dropout, LSTM
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class Model():
	"""A class for an building and inferencing an lstm model"""

	def __init__(self):
		self.model = Sequential()

	def load_model(self, filepath):
		print('[Model] Loading model from file %s' % filepath)
		self.model = load_model(filepath)

	def build_model(self, configs):
		timer = Timer()
		timer.start()

		for layer in configs['model']['layers']:
			neurons = layer['neurons'] if 'neurons' in layer else None
			dropout_rate = layer['rate'] if 'rate' in layer else None
			activation = layer['activation'] if 'activation' in layer else None
			return_seq = layer['return_seq'] if 'return_seq' in layer else None
			input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
			input_dim = layer['input_dim'] if 'input_dim' in layer else None

			if layer['type'] == 'dense':
				self.model.add(Dense(neurons, activation=activation))
			if layer['type'] == 'lstm':
				self.model.add(LSTM(neurons, input_shape=(input_timesteps, input_dim), return_sequences=return_seq))
			if layer['type'] == 'dropout':
				self.model.add(Dropout(dropout_rate))

		self.model.compile(loss=configs['model']['loss'], optimizer=configs['model']['optimizer'], metrics=['accuracy'])

		print('[Model] Model Compiled')
		timer.stop()

	def train(self, x, y, configs_train, validation_data, verbose='auto'):
		timer = Timer()
		timer.start()

		epochs = configs_train['epochs']
		batch_size = configs_train['batch_size']
		monitor = configs_train['monitor']
		patience = configs_train['patience']
		save_dir = configs_train['model_save_dir']

		print('[Model] Training Started')
		print('[Model] %s epochs, %s batch size' % (epochs, batch_size))
		
		
		save_fname = 'epoch{epoch:02d}-acc{val_accuracy:.2f}-loss{val_loss:.2f}.h5'
		save_fname = os.path.join(save_dir, '%s-%s' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(save_fname)))
		callbacks = [
			EarlyStopping(monitor=monitor, patience=patience, restore_best_weights=True),
			ModelCheckpoint(filepath=save_fname, monitor=monitor, save_best_only=True)
		]
		history = self.model.fit(
			x,
			y,
			epochs=epochs,
			batch_size=batch_size,
			callbacks=callbacks,
			#validation_split=0.10
			validation_data = validation_data,
			verbose = verbose
		)

		# save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		# self.model.save(save_fname)

		print('[Model] Training Completed. Model saved as %s' % save_fname)
		timer.stop()

		return history

	def train_generator(self, data_gen, epochs, batch_size, steps_per_epoch, save_dir):
		timer = Timer()
		timer.start()
		print('[Model] Training Started')
		print('[Model] %s epochs, %s batch size, %s batches per epoch' % (epochs, batch_size, steps_per_epoch))
		
		save_fname = os.path.join(save_dir, '%s-e%s.h5' % (dt.datetime.now().strftime('%d%m%Y-%H%M%S'), str(epochs)))
		callbacks = [
			ModelCheckpoint(filepath=save_fname, monitor='loss', save_best_only=True)
		]
		self.model.fit_generator(
			data_gen,
			steps_per_epoch=steps_per_epoch,
			epochs=epochs,
			callbacks=callbacks,
			workers=1
		)
		
		print('[Model] Training Completed. Model saved as %s' % save_fname)
		timer.stop()

	def predict_point_by_point(self, data):
		#Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
		print('[Model] Predicting Point-by-Point...')
		predicted = self.model.predict(data)
		predicted = np.reshape(predicted, (predicted.size,))
		return predicted

	def predict_sequences_multiple(self, data, window_size, prediction_len):
		#Predict sequence of <prediction_len> steps before shifting prediction run forward by <prediction_len> steps
		print('[Model] Predicting Sequences Multiple...')
		prediction_seqs = []
		for i in range(int(len(data)/prediction_len)):
			curr_frame = data[i*prediction_len]
			predicted = []
			for j in range(prediction_len):
				predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])
				curr_frame = curr_frame[1:]
				curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)
			prediction_seqs.append(predicted)
		return prediction_seqs

	def predict_sequence_full(self, data, window_size):
		#Shift the window by 1 new prediction each time, re-run predictions on new window
		print('[Model] Predicting Sequences Full...')
		curr_frame = data[0]
		predicted = []
		for i in range(len(data)):
			predicted.append(self.model.predict(curr_frame[newaxis,:,:])[0,0])
			curr_frame = curr_frame[1:]
			curr_frame = np.insert(curr_frame, [window_size-2], predicted[-1], axis=0)
		return predicted

	def predict_sequences_sample_tbl(self, data, prediction_len, verbose='auto'):
		#Predict TBL and shifts prediction run forward by <prediction_len> steps
		# First prediction is made with <prediction_len> history
		print('[Model] Predicting Sequences Multiple TBL ...')
		prediction_seqs = []
		for i in range(int(len(data)/prediction_len)):
			curr_frame = data[i*prediction_len]
			predicted = []
			predicted.append(self.model.predict(curr_frame[newaxis,:,:],verbose=verbose))
			prediction_seqs.append(predicted)
		return prediction_seqs
	
	def predict_sequence_full_tbl(self, data, verbose='auto'):
		#Predict TBL and shifts prediction run forward by <prediction_len> steps
		# First prediction is made with <prediction_len> history
		print('[Model] Predicting Sequences Multiple TBL ...')
		prediction_seqs = []
		for i in range(int(len(data))):
			curr_frame = data[i]
			predicted = []
			predicted.append(self.model.predict(curr_frame[newaxis,:,:],verbose=verbose))
			prediction_seqs.append(predicted)
		return np.array(prediction_seqs).reshape(len(prediction_seqs),3)

	# def predict_today_tbl(self, data):
	# 	#Predict TBL and shifts prediction run forward by <prediction_len> steps
	# 	# First prediction is made with <prediction_len> history
	# 	curr_frame = data[i]
	# 	predicted = []
	# 	predicted.append(self.model.predict(curr_frame[newaxis,:,:]))
	# 	prediction_seqs.append(predicted)
	# 	return np.array(prediction_seqs).reshape(len(prediction_seqs),3)


	# def predict_point_by_point(self, data):
	# 	#Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
	# 	print('[Model] Predicting Point-by-Point...')
	# 	predicted = self.model.predict(data)
	# 	predicted = np.reshape(predicted, (predicted.size,))
	# 	return predicted