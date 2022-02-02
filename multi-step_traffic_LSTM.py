# univariate multi-step vector-output stacked lstm example
from numpy import array
from numpy import asarray
from numpy import savetxt
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import csv
import matplotlib.pyplot as plt
import time

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

start_time = time.perf_counter()

with open("traffic_data_real.csv", newline = '') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter = ' ')
	traffic_data = []
	for item in csv_reader:
		traffic_data.append(int(item[0]))
csv_file.close()

# define input sequence
sample_size = 96*7
raw_seq = traffic_data[0:sample_size]

#for n_steps_in in range(2,48,2):
# choose a number of time steps
n_steps_in = 16
n_steps_out = 96
# split into samples
X, y = split_sequence(raw_seq, n_steps_in, n_steps_out)
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))
# define model
model = Sequential()
model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
model.add(LSTM(100, activation='relu'))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X, y, epochs=50, verbose=0)
# demonstrate prediction
x_input = array(raw_seq[sample_size-n_steps_in:sample_size])
x_input = x_input.reshape((1, n_steps_in, n_features))
yhat = model.predict(x_input, verbose=0)
#print(yhat)

savetxt(f'{n_steps_in}_steps_in_{sample_size}_sample_predicted.csv',asarray(yhat),delimiter=',')
savetxt(f'{n_steps_in}_steps_in_{sample_size}_sample_real.csv',asarray([traffic_data[sample_size:sample_size+n_steps_out]]),delimiter=',')

end_time = time.perf_counter()

print(f"TIME TAKEN: {end_time-start_time} seconds")

plt.plot([i for i in range(1,len(traffic_data[sample_size:sample_size+n_steps_out])+1)], traffic_data[sample_size:sample_size+n_steps_out], [i for i in range(1,len(yhat[0])+1)], yhat[0])
plt.xlabel("Data Points (every 15 minutes)")
plt.ylabel("Traffic (number of cars)")
plt.savefig(f'{n_steps_in}_steps_in_{sample_size}_sample.png')
plt.clf()