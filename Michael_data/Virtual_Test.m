clear
clc
clf
close all

% load the trained DQN
load('trained_DQN.mat')

S_memo=200;

Rmemo=zeros(10,S_memo);         
Memopointer=1;                  

Rmemo_next=zeros(10,S_memo);     
Memopointer_next=1;             

% thisEpisode = unidrnd(16800)+200; 
% Here you can select a number from 200-16800, not just 3031 
% one year = 8760 hours = 17520 half an hours, we get rid of the first and
% last days
thisEpisode = 3031;
endEpisode = thisEpisode + T_episode - 1;
BatterySoC = PV_Power(ceil(thisEpisode/2)).battery;

index = 1;
Total_Carbon = 0;
Total_Price = 0;

% data processing
for i = thisEpisode:(endEpisode+1)
    PV_Power_episode(index).Carbon_Real = Carbon_data(i).RealCarbon;
    PV_Power_episode(index).Carbon_Pred = Carbon_data(i).Predicted_Carbon;
    PV_Power_episode(index).Hour = Carbon_data(i).HourChanged;
    PV_Power_episode(index).ElecUsed = Streetdata(i).PVConsumption_half_hour;
    PV_Power_episode(index).PV_Real = YTest_Changed(i);
    PV_Power_episode(index).PV_Pred = YPred_Changed(i);
    PV_Power_episode(index).BatterySoC = PV_Power(ceil(i/2)).battery;
    PV_Power_episode(index).Rank = Carbon_data(i).find_Carbon;
    PV_Power_episode(index).Price = Pricedata_origion(i).Total_half_hour;
    PV_Power_episode(index).PriceRank = Pricedata_origion(i).Price_count;
    
    index = index + 1;
end
PV_Power_episode_standard = dataStandardized_Train(thisEpisode:(endEpisode+1),:);
Carbon_rank = Carbon_data_at_double(thisEpisode:(endEpisode+1),:);
Price_elec = Pricedata_double(thisEpisode:(endEpisode+1),:);
Price_rank = Pricedata_at_double(thisEpisode:(endEpisode+1),:);

% DQN algorithm
for Tm=1:T_episode
    % see Energy_allocation_tcegreedy function 
    [Qmax,flag,Memory]=Energy_allocation_tcegreedy(Ts,QNet_eval,PV_Power_episode(Tm),PV_Power_episode_standard(Tm,:),BatterySoC,mu_This(7),sig_This(7),Carbon_rank(Tm),Price_elec(Tm),Price_rank(Tm));     
    EnergyBought = Memory(9);             
    Battery_or_Grid = Memory(10);    
    % see Energy_allocation_movement function
    [EnergyChanged,CarbonProduced,Price_Paid]=Energy_allocation_movement(EnergyBought,Battery_or_Grid,BatterySoC,PV_Power_episode(Tm));
    BatterySoC = EnergyChanged;
    Total_Carbon = Total_Carbon + CarbonProduced;
    Total_Price = Total_Price + Price_Paid;
    % This is 'memeory reply' in DQN, learn DQN and you will know what is
    % that, as well as eplison-greedy algorithm
    Rmemo(1:10,Memopointer)=Memory;        
    Memopointer=Energy_allocation_pointermove(Memopointer,S_memo);

    PV_Power_next=PV_Power_episode_standard(Tm+1,:);
    Carbon_rank_get=Carbon_rank(Tm+1);
    Carbon_Pred_Norm_next=PV_Power_next(2);
    Hour_next=PV_Power_next(3);
    Elec_Used_Norm_next=PV_Power_next(4);
    PV_Pred_Norm=PV_Power_next(6);
    CurrentBatterySoC_Norm = (BatterySoC - mu_This(7)) ./ sig_This(7);
    Memory_next=[Carbon_Pred_Norm_next;Hour_next;Elec_Used_Norm_next;PV_Pred_Norm;CurrentBatterySoC_Norm;Qmax];
    Rmemo_next(1:6,Memopointer_next)=Memory_next;
    Rmemo_next(7,Memopointer_next)=BatterySoC;
    Rmemo_next(8,Memopointer_next)=Carbon_rank_get;
    Rmemo_next(9,Memopointer_next)=Price_elec(Tm+1);
    Rmemo_next(10,Memopointer_next)=Price_rank(Tm+1);

    Memopointer_next=Energy_allocation_pointermove(Memopointer_next,S_memo);
end

% anti-normalization
Rmemo_backup(1:5,:) = sig_nor_selected.*Rmemo(1:5,:) + mu_nor_selected;
Rmemo_backup(6,:) = Carbon_sig.*Rmemo(6,:) + Carbon_mu;
Rmemo_backup(7,:) = Price_sig.*Rmemo(7,:) + Price_mu;
Rmemo_backup(8,:) = Price_at_sig.*Rmemo(8,:) + Price_at_mu;
Rmemo_backup(9:10,:) = Rmemo(9:10,:);

All_the_data2(1:5,:) = Rmemo_backup(1:5,:);
All_the_data2(6,:) = Rmemo_backup(7,:);
All_the_data2(7,:) = Rmemo_backup(9,:);
All_the_data2(8,:) = Rmemo_backup(10,:);

% 1. Carbon_Real_Norm: Carbon emission dataset in this half an hour 
% 2. This_Hour_Norm: What is the hour of the day
% 3. Elec_Used_Norm: How much electricity should we use for the LED light in this half an hour
% 4. PV_Real_Norm: How much electricity is generated from the PV panel in this half an hour 
% 5. CurrentBatterySoC_Norm: Current Battery SoC/energy in this half an hour
% 6. Carbon_rank: the rank of Carbon emission 
% 7. Price_elec: Electricity Price dataset in this half an hour
% 8. Price_rank: the rank of Electricity Price
% 9. Elec_Buy: Based on DQN, how much electricity should we buy in this half an hour
% 10. Battery_or_Grid: Should the LED light use power grid electricity or the battery in this half an hour

% Try to comment/delete it, see what will happen?
load('paper_test.mat')

j = 1:200;
subplot(3,1,1)
plot(j,Rmemo_backup(1,:),'-r');
ylabel({'Carbon Emission','Intensity (gCO2/kWh)'},'color','k','fontsize',8);
axis([0 200,0 400])

subplot(3,1,2)
plot(j,Rmemo_backup(7,:),'-k');
ylabel({'Electricity','Price (Euro/MWh)'},'color','k','fontsize',9);

subplot(3,1,3)
plot(j,Rmemo_backup(9,:),'-b');
ylabel({'Net Power Demand','from Grid with DQN (4Ah)'},'color','k','fontsize',8);

xlabel('Number of half-an-hours','color','k','fontsize',10);

total_demand = 0;
total_Carbon_Cal = 0;
total_Price_Cal = 0;

for i = 1:201
    total_demand = total_demand + PV_Power_episode(i).ElecUsed;
    total_Carbon_Cal = total_Carbon_Cal + (PV_Power_episode(i).ElecUsed * PV_Power_episode(i).Carbon_Real)/1000;
    total_Price_Cal = total_Price_Cal + (PV_Power_episode(i).ElecUsed * PV_Power_episode(i).Price)/1000;
end



