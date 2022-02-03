import numpy as np
import math
import csv
import matplotlib.pyplot as plt

def open_csv(steps_in,sample_size,type):
    with open(f"{steps_in}_steps_in_{sample_size}_sample_{type}.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ' ')
        data = []
        for row in csv_reader:
            data = row[0].split(',')
        data = [float(i) for i in data]
    csv_file.close()
    return data

steps_in_plot = []
RMSE_plot = []
steps_in = 15
RMSE_array = []
for sample_size in range(96*7,96*7*52,96*7*13):
    real_data = open_csv(str(steps_in),sample_size,"real")
    predicted_data = open_csv(str(steps_in),sample_size,"predicted")
    MSE = np.square(np.subtract(real_data,predicted_data)).mean()
    RMSE = math.sqrt(MSE)
    RMSE_array.append(RMSE)
if not np.any(np.isnan(RMSE_array)):
    steps_in_plot.append(steps_in)
    RMSE_plot.append(np.average(RMSE_array))

print(steps_in_plot)
print(RMSE_plot)
plt.scatter(steps_in_plot,RMSE_plot)
plt.xticks(range(min(steps_in_plot), max(steps_in_plot)+1, 2))
plt.xlabel("Number of Steps In")
plt.ylabel("Average RMSE (Root Mean Squared Error)")
plt.savefig(f"LSTM_RMSE_{steps_in}_steps_in.png")
plt.clf()