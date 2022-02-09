% after making decision from the function Energy_allocation_tcegreedy, Energy_allocation_movement do the real move for the battery energy. 
% update the battery energy with this function.
%%%%% Input: 
% EnergyBought, how much energy should we bought in this half an hour
% Battery_or_Grid: Use battery or main grid to power the LED
% BatterySoC: Current battery Soc
%%%%% Output：
% EnergyChanged: energy we should bought
% CarbonProduced: Carbon Produced in this half an hour
% Price_Paid: How much should we pay in this half an hour
function [EnergyChanged,CarbonProduced,Price_Paid]=Energy_allocation_movement(EnergyBought,Battery_or_Grid,BatterySoC,PV_Power_episode) 
    MaximumAh = 4;
    Carbon_this_hour = PV_Power_episode.Carbon_Real;
    Price_this_hour = PV_Power_episode.Price;
    % Use battery to power the LED
    if Battery_or_Grid == 1
        CarbonProduced_bought = Carbon_this_hour*EnergyBought*MaximumAh*12/1000;
        Price_Paid = Price_this_hour*EnergyBought*MaximumAh*12/1000;
        CarbonProduced = CarbonProduced_bought;
        EnergyChanged = BatterySoC + EnergyBought*MaximumAh*12*0.9 - PV_Power_episode.ElecUsed + PV_Power_episode.PV_Real;
        if EnergyChanged >= 2400
            EnergyChanged = 2400;
        end
        if EnergyChanged <= 0
            EnergyChanged = 0;
        end
    % Use Grid to power the LED    
    elseif Battery_or_Grid == 2
        CarbonProduced_bought = Carbon_this_hour*EnergyBought*MaximumAh*12/1000;
        Price_Paid = Price_this_hour*EnergyBought*MaximumAh*12/1000;
        CarbonProduced_use = Carbon_this_hour*PV_Power_episode.ElecUsed/1000;
        CarbonProduced = CarbonProduced_bought+CarbonProduced_use;
        EnergyChanged = BatterySoC + EnergyBought*MaximumAh*12*0.9 + PV_Power_episode.PV_Real;
        if EnergyChanged >= 2400
            EnergyChanged = 2400;
        end
    end
    
end


