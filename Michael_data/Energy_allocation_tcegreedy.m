% This is the eplison-greedy algorithm in DQN
% In different situations, which choice is better.
%%%%% Input: 
% QNet: trained DQN
% others: different paremeters that the DQN will use
%%%%% Output：
% Memory: the best choice
% Qmax: Q valuue with the best choice
function [Qmax,flag,Memory]=Energy_allocation_tcegreedy(Ts,QNet,~,PV_Power_episode_standard,BatterySoC,mu_This,sig_This,Carbon_rank,Price_elec,Price_rank) 
global EnergyFromPowerGrid;

Carbon_Real_Norm = PV_Power_episode_standard(1);
This_Hour_Norm = PV_Power_episode_standard(3);
Elec_Used_Norm = PV_Power_episode_standard(4);
PV_Real_Norm = PV_Power_episode_standard(5);

CurrentBatterySoC_Norm = (BatterySoC - mu_This) ./ sig_This;

Memory=[];  

P_e=rand(1);
if P_e < (1/(Ts^0.2))||Ts <= 100              

    if BatterySoC >= 2400*0.9 && unidrnd(1) >= 0.5 
        Elec_Buy = 0;
    else
        Elec_Buy = unidrnd(EnergyFromPowerGrid);
    end
    if BatterySoC <= 2400*0.1
        Battery_or_Grid = 2;              
    else
        Battery_or_Grid = unidrnd(2);   
    end

    dataStandardized_Greedy = [Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;Elec_Buy;Battery_or_Grid];
    Memory=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;Elec_Buy;Battery_or_Grid];
    Qmax = QNet(dataStandardized_Greedy);  
    flag = 4;
else                                      
    if BatterySoC >= 2400*0.9
        flag = 1;

        Input1(:,1)=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;0;1];
        Input1(:,2)=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;0;2];
        Input(:,1)=[Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;0;1];
        Input(:,2)=[Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;0;2];
    elseif BatterySoC >= 2400*0.1
        flag = 2;
        numbers = 0;
        for j = 0:EnergyFromPowerGrid
            numbers = numbers + 1;
            Input1(:,numbers)=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;1];
            Input(:,numbers)=[Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;1];
        end
        for j = 0:EnergyFromPowerGrid
            numbers = numbers + 1;
            Input1(:,numbers)=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;2];
            Input(:,numbers)=[Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;2];
        end
    else
        flag = 3;
        for j = 0:EnergyFromPowerGrid
            Input1(:,j+1)=[Carbon_Real_Norm;This_Hour_Norm;Elec_Used_Norm;PV_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;2];
            Input(:,j+1)=[Carbon_Real_Norm;CurrentBatterySoC_Norm;Carbon_rank;Price_elec;Price_rank;j;2];
        end
    end
       
    
    Q0=QNet(Input);
    Qmax=-inf;
    
    if flag == 1
        for i=1:2
            if Qmax<Q0(i)
                Qmax=Q0(i);
                Memory=Input1(:,i);
            end
        end
    elseif flag == 2
        for i=1:12
            if Qmax<Q0(i)
                Qmax=Q0(i);
                Memory=Input1(:,i);
            end
        end
    elseif flag == 3
        for i=1:6
            if Qmax<Q0(i)
                Qmax=Q0(i);
                Memory=Input1(:,i);
            end
        end
    end
    
end


