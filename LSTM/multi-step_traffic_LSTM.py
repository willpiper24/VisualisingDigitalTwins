# univariate multi-step vector-output stacked lstm example
from datetime import datetime, timedelta
import numpy as np
from numpy import array
from numpy import asarray
from numpy import savetxt
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.metrics import mean_absolute_percentage_error
import csv
import matplotlib.pyplot as plt
import time
from datetime import date, datetime
import math

# split a univariate sequence into samples
def split_sequence(sequence, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the sequence
		if out_end_ix > len(sequence):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

def run_LSTM(X, y, raw_seq, n_steps_in, n_steps_out, n_features):
	model = Sequential()
	model.add(LSTM(200, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
	model.add(LSTM(200, activation='relu'))
	model.add(Dense(n_steps_out))
	model.compile(optimizer='adam', loss='mse')
	# fit model
	model.fit(X, y, epochs=200, verbose=0)
	# demonstrate prediction
	x_input = array(raw_seq[-1-n_steps_in:-1])
	x_input = x_input.reshape((1, n_steps_in, n_features))
	yhat = model.predict(x_input, verbose=0)
	return yhat

with open("traffic_data_real.csv", newline = '') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter = ' ')
	traffic_data = []
	for item in csv_reader:
		traffic_data.append(int(item[0]))
csv_file.close()

# define input sequence
#sample_size = 96*7*4
#raw_seq = traffic_data[0:sample_size]

RMSE_values = {}
MAPE_values = {}
for i in range(0,1):
	now = datetime.now() + timedelta(days=i) + timedelta(hours=i*4)

	t0 = datetime(2019,1,1,0,0,0)
	t1 = datetime(2019,date.today().month,date.today().day,now.hour,now.minute,now.second)
	total_seconds = (t1-t0).total_seconds()

	sample_size = math.floor(total_seconds/(15*60))-2
	#sample_size = 35039
	start_index = sample_size-(96*7*4)
	if start_index < 0:
		raw_seq	= traffic_data[start_index:0] + traffic_data[0:sample_size]
	else:
		raw_seq = traffic_data[start_index:sample_size]

	start_time = time.perf_counter()

	# choose a number of time steps
	n_steps_in = 15
	n_steps_out = 48
	# split into samples
	X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
	# reshape from [samples, timesteps] into [samples, timesteps, features]
	n_features = 1
	X = X.reshape((X.shape[0], X.shape[1], n_features))

	yhat = run_LSTM(X, y, raw_seq, n_steps_in, n_steps_out, n_features)

	#savetxt(f'{n_steps_in}_steps_in_{sample_size}_sample_predicted.csv',asarray(yhat),delimiter=',')
	#savetxt(f'{n_steps_in}_steps_in_{sample_size}_sample_real.csv',asarray([traffic_data[sample_size:sample_size+n_steps_out]]),delimiter=',')
	savetxt('LSTM_data.csv',asarray(yhat),delimiter=',')

	RMSE_array = []
	RMSE_plot = []
	predicted_data = yhat[0]
	real_data = traffic_data[sample_size:sample_size+n_steps_out]
	MSE = np.square(np.subtract(real_data,predicted_data)).mean()
	RMSE = math.sqrt(MSE)
	loss = mean_absolute_percentage_error(real_data, predicted_data)
	RMSE_values[f'{i}'] = RMSE
	MAPE_values[f'{i}'] = loss.numpy()

	end_time = time.perf_counter()

	print(f"TIME TAKEN: {end_time-start_time} seconds")

	plt.plot([i*15 for i in range(1,len(real_data)+1)], real_data, [i*15 for i in range(1,len(yhat[0])+1)], yhat[0])
	plt.xlabel("Time (minutes)")
	plt.ylabel("Traffic (number of cars)")
	plt.legend(['Real','Predicted'], loc='upper right')
	plt.show()
	#plt.savefig(f'real_vs_predicted_{i}.png')
	plt.clf()

#print(RMSE_values)
#print(MAPE_values)