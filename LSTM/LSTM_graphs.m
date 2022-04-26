clear
clc
clf
close all

real_data_0 = readmatrix('LSTM_data_real_0.csv');
predicted_data_0 = readmatrix('LSTM_data_predicted_0.csv');
real_data_1 = readmatrix('LSTM_data_real_2.csv');
predicted_data_1 = readmatrix('LSTM_data_predicted_2.csv');
x_trans = readmatrix('LSTM_x_axis_0.csv');
x = x_trans';

subplot(2,1,1)
hold on
plot(x,real_data_0','LineWidth',1);
plot(x,predicted_data_0,'LineWidth',1);
hold off
legend('Real','Predicted','Location','northeast','fontsize',12)
ylabel({'Traffic','(number of cars)'},'fontsize',13);
ylim([0 320])
xlim([15 720])

subplot(2,1,2)
hold on
plot(x,real_data_1','LineWidth',1);
plot(x,predicted_data_1,'LineWidth',1);
hold off
legend('Real','Predicted','Location','northeast','fontsize',12)
ylabel({'Traffic','(number of cars)'},'fontsize',13);
ylim([0 320])
xlim([15 720])

xlabel('Time From Present (minutes)','fontsize',14);

exportgraphics(gcf,'LSTM_graphs.png','Resolution',500)