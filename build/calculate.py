import pandas as pd

def hours_to_floats(start,end):
    start_hour, start_min = list(map(int,start.split(":")))
    end_hour, end_min = list(map(int,end.split(":")))

    start = start_hour + start_min/60
    end = end_hour + end_min/60

    if end<start:
        end += 24
    return start,end

def get_shift_multiplier(hour, base_multiplier):
    multiplier = 1

    #30% between 18-22 (6pm-10pm) 
    if 17< hour <= 21:
        multiplier += 0.3

    #40% after 22 (10pm)
    elif 21< hour: 
        multiplier += 0.4

    return multiplier

def is_weekend(year,month,day):
    return pd.to_datetime(f'{year}-{month}-{day}').weekday() > 4

def get_daily_wage(year,date,workhours,hourly_wage):
    month,day = date
    start,end = workhours
    daily_wage = 0
    hours_worked = 0
    base_multiplier = 1


    if is_weekend(year,month,day):
        base_multiplier += 0.2

    hour = start
    while True:
        #if the employee works over 6 hours, they have a break, which counts as 0.5 hour worked off after the 2nd hour and will also be added to the workours
        #break time gets the multiplier of the 2nd hour
        #if 2nd hour is between 17:00-18:00 and has 1x multiplier (no bonus)
        #then break takes time between 18:00-18:30 and has 1x multiplier: ignores the shift allowance bonus

        multiplier = get_shift_multiplier(hour, base_multiplier)
        
        hour += 1

        if hour > end:
            daily_wage += ((1 - (hour-end) ) * hourly_wage * multiplier)
            hours_worked += (1 - (hour-end) )
            if end-start > 6:
                hours_worked -= (1/3)
                #daily_wage += 0.5 * multiplier * hourly_wage
                #print(hourly_wage, multiplier, hourly_wage * multiplier * 0.5)

            return daily_wage,hours_worked
        
        daily_wage += hourly_wage * multiplier
        #print(hourly_wage, multiplier, hourly_wage * multiplier)
        hours_worked += 1
        

#print(get_daily_wage('2024',['5','1'],[11.0, 18.5], 1540))
#exit()



#def getIncome(year,month,hourly_wage):
def getIncome(year,month, hourly_wage):
    total_hours_worked = 0
    total_wage = 0

    #reading the excel sheet named after the year
    with pd.ExcelFile('Workdays.xlsx') as ws:
        file = pd.read_excel(ws, sheet_name=year)

    #Listing all months to help reading the file
    all_months = [x for x in file][1::]
    
    #option to calculate whole year's income if no months were given
    if len(month)==0:
        months = all_months
    else:
        months = [month]
    
    for month_ in months:
        if month_[-1] == ".":
            month_ = month[0:-1]
        if month_.isdigit() and int(month_) < 13:
            month_data = file[all_months[int(month_)-1]]
        elif type(month_) == str and month_ in all_months:
            month_data = file[month_]
        
        #extrating data from the month's column
        #elements  ----> [['4', 1], ['18:00', '1:30']] = [[month, day], [start,end]]
        workdays = []
        for i,workday in enumerate(month_data):
            if str(workday) != 'nan':
                workdays.append([[month,i+1],workday.split("-")])
        

        monthly_hours_worked = 0
        monthly_wage = 0

        for date, workhours in workdays:
            workhours = hours_to_floats(workhours[0], workhours[1])
            daily_wage,daily_hours_worked = get_daily_wage(year,date,workhours,hourly_wage)
            monthly_wage += daily_wage
            monthly_hours_worked += daily_hours_worked

        
        if monthly_hours_worked >= 150:
            monthly_wage += 300*monthly_hours_worked
            monthly_wage += 6770
        elif monthly_hours_worked >= 120:
            monthly_wage += 250*monthly_hours_worked
            monthly_wage += 6015
        elif monthly_hours_worked >= 100:
            monthly_wage += 210*monthly_hours_worked
        elif monthly_hours_worked >= 80:
            monthly_wage += 160*monthly_hours_worked
        elif monthly_hours_worked >= 40:
            monthly_wage += 120*monthly_hours_worked

        total_hours_worked += monthly_hours_worked
        total_wage += monthly_wage

    return total_hours_worked,total_wage
        
        
        




'''print(getIncome('2024', '1', 1540))


def f(cash, hour):
    without_bonus = (hour/3 * 1.3 * 1540 + 2*hour/3 * 1540)
    bonus = cash - without_bonus
    print(f"Bonus after {hour} hours: {bonus} \t\t Multiplier: {cash/without_bonus}")

f(50820, 30)
f(72560, 40)
f(148320, 80)
f(190400, 100)
f(233280, 120)
f(334990, 168)'''
