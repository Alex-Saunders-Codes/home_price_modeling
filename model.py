#Model
from __main__ import *

#Global Paramaters
#Amount of time to model
time = inputs['Duration in Years']
#Housing budget avaliable
total_available = inputs['Monthly Housing Budget'] * 12
#Monthly amount paid for a house
home_cost = inputs["Monthly Home Cost"]
#Principal and Interest Payment is monthly mortgage minus the portion that goes to extras
principal_and_interest = inputs["Monthly Home Cost"] - inputs["Mortgage Extras"]

#House related parameters
#Total Home Value
original_home_value = inputs["Home Value"]
#Down payment
down_payment = inputs["Down Payment"]
#Initial house costs
house_fees = inputs["Home Purchase Fees"]   
#Mortgage loan interest
interest_rate = inputs["Mortgage Interest Rate"]    
#House Appreciation
home_value_increase = inputs["Rate of Home Appreciation"]


#Rent related parameters 
#rent cost
rent_cost = inputs["Rent"]   
#Expected annual increase in rent
rent_increase = inputs["Rate of Rent Increase"]


#Investment related parameters
#Amount invested
starting_investments = inputs["Starting Investments"]
#Average stock market return
market_return = inputs["Rate of Market Return"]


#Construct first line of table
def model():
#Calculate total annual housing cost
    annual_home_cost = home_cost*12

    #Calculate annual rent
    annual_rent_cost = rent_cost *12

    #Calculate starting investments
    investments = starting_investments - down_payment - house_fees

    #Calculate mortgage loan
    original_mortgage = original_home_value - down_payment

    years = []
    years.append({
             'home_value': original_home_value,
             'home_cost': annual_home_cost + original_home_value * .022,
             'rent_cost': annual_rent_cost,
             'mortgage': original_mortgage,
             'home_equity': down_payment,
             'investments': investments, 
             'gross': down_payment + investments,
        })


while len(years) <= time:
    years.append(one_year(years[-1], inputs))
return years

def one_year(previous_year, inputs):
    
    #House Appreciation
    home_value_increase = inputs["Rate of Home Appreciation"]
    #Total Home Value
    original_home_value = inputs["Home Value"]
    #Calculate total annual housing cost
    annual_home_cost = home_cost*12

    #Calculate annual rent
    annual_rent_cost = rent_cost *12

    new_home_value = previous_year['home_value'] + np.standard_gamma(home_value_increase*100)/80 * previous_year['home_value']
   
    #Allocate 1% of home value to repairs annually, 1.2% in expected property taxes
    new_home_cost = annual_home_cost + new_home_value * .022

    new_rent_cost = previous_year['rent_cost'] + np.standard_gamma(rent_increase*100)/80 * previous_year['rent_cost']
    
    new_mortgage = amortization(previous_year['mortgage'])
    
    new_home_equity = previous_year['home_equity'] + (previous_year['mortgage'] - new_mortgage)
   
    total_investments = previous_year['investments'] + (previous_year['investments'] * np.normal(market_return, .04, 1)) + (total_available - (new_rent_cost + new_home_cost)) 
    
    new_gross = total_investments + (new_home_value - original_home_value) + new_home_equity
    
    new_year = {
             'home_value': new_home_value,
             'home_cost': new_home_cost,
             'rent_cost': new_rent_cost,
             'mortgage': new_mortgage,
             'home_equity': new_home_equity,
             'investments': total_investments, 
             'gross': new_gross[0],
        }
    return new_year


def amortization(mortgage):
    month = 0
    monthly_interest = interest_rate/12
    while month < 12:
        #Generate an amount paid towards interest each month
        interest_payment = mortgage * monthly_interest
        new_equity = principal_and_interest - interest_payment
        mortgage = mortgage - new_equity
        month += 1
        
    return mortgage
