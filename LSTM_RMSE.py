import numpy as np
import math
import csv
import matplotlib.pyplot as plt

def open_csv(steps_in,type):
    with open(steps_in + "_steps_in_" + type + ".csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ' ')
        data = []
        for row in csv_reader:
            data = row[0].split(',')
        data = [float(i) for i in data]
    csv_file.close()
    return data

steps_in_plot = []
RMSE_plot = []
for steps_in in range(2,48,2):
    real_data = open_csv(str(steps_in),"real")
    predicted_data = open_csv(str(steps_in),"predicted")
    if not np.any(np.isnan(predicted_data)):
        MSE = np.square(np.subtract(real_data,predicted_data)).mean()
        RMSE = math.sqrt(MSE)
        RMSE_plot.append(RMSE)
        steps_in_plot.append(steps_in)

print(steps_in_plot)
print(RMSE_plot)
plt.scatter(steps_in_plot,RMSE_plot)
plt.xticks(range(min(steps_in_plot), max(steps_in_plot)+1, 2))
plt.xlabel("Number of Steps In")
plt.ylabel("RMSE (Root Mean Squared Error)")
plt.savefig("LSTM_RMSE.png")