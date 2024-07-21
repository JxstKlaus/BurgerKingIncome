import pandas as pd

#converts workhours to floats
def hoursToNumbers(start,end):
    start = list(map(int,start.split(":")))
    end = list(map(int,end.split(":")))

    start = start[0]+start[1]/60
    end = end[0]+end[1]/60

    if end<start:
        end += 24
    return start,end


#checks if the day is a weekend or not
def isWeekend(year,month,day):
    return pd.to_datetime(f'{year}-{month}-{day}').weekday() > 4

#shift allowance bonus
def shiftAllowance(hour,multiplier):
    #30% between 18-22 (6pm-10pm) 
    if 17< hour <= 21:
        if hour < 18:
            #17:01-18:00 no bonus 
            mins_after_hour = hour-int(hour)
            multiplier = (1-mins_after_hour)*multiplier + mins_after_hour*(multiplier+0.3)
        else:
            multiplier += 0.3

    #40% after 22 (10pm)
    elif 21< hour: 
        if hour < 22:
            #21:01-22:00 30% bonus
            mins_after_hour = hour-int(hour)
            multiplier = (1-mins_after_hour)*(multiplier+0.3) + mins_after_hour*(multiplier+0.4)
        else:
            multiplier += 0.4
    return multiplier

#calculates daily wage
def dailyWage(year,date,workhours,hourly_wage):
    month,day = date
    start,end = workhours
    daily_wage = 0
    hours_worked = 0
    daily_break = 0

    #Weekend bonus 10%
    if isWeekend(year,month,day):
        base_multiplier = 1.1
    else:
        base_multiplier = 1

    hour = start

    while True:
        #if the employee works over 6 hours, they have a break, which counts as 0.5 hour worked off after the 2nd hour and will also be added to the workours
        #break time gets the multiplier of the 2nd hour
        #if 2nd hour is between 17:00-18:00 and has 1x multiplier (no bonus)
        #then break takes time between 18:00-18:30 and has 1x multiplier: ignores the shift allowance bonus
        if end-start > 6 and hour - start == 3:
             multiplier = shiftAllowance(int(hour),base_multiplier)
             break_time = 0.5
             daily_wage += break_time * hourly_wage * base_multiplier
             hours_worked += break_time
             hour += break_time
             #end -= break_time
             daily_break = 1
        
        multiplier = shiftAllowance(hour,base_multiplier)
        
        if hour > end:
            daily_wage -= ((hour-end) * hourly_wage * multiplier)
            hours_worked -= hour-end
            break

        daily_wage += hourly_wage * multiplier
        hour += 1
        hours_worked += 1
    return daily_wage,hours_worked, daily_break

#main func
def getIncome(year,month,hourly_wage):
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

    #iterating through the months
    for month in months:
        if month[-1] == ".":
            month = month[0:-1]
        if month.isdigit() and int(month) < 13:
            month_data = file[all_months[int(month)-1]]
        elif type(month) == str and month in all_months:
            month_data = file[month]
        
        #extrating data from the month's column
        workdays = []
        for i,workday in enumerate(month_data):
            if str(workday) != 'nan':
                workdays.append([[month,i+1],workday.split("-")])
        
        monthly_break_count = 0
        monthly_hours_worked = 0
        monthly_wage = 0

        for date,workhours in workdays:
            workhours = hoursToNumbers(workhours[0],workhours[1])
            daily_wage,daily_hours_worked,daily_break = dailyWage(year,date,workhours,hourly_wage)
            monthly_wage += daily_wage
            monthly_hours_worked += daily_hours_worked
            monthly_break_count += daily_break

        #monthly bonuses are based on the worked off hours: breaks don't count in --> (monthly_hours_worked - monthly_break_count*(1/3))
        worked_off_hours = monthly_hours_worked - monthly_break_count*(1/3)

        if worked_off_hours > 150:
            monthly_wage += 300*worked_off_hours
        elif worked_off_hours > 120:
            monthly_wage += 250*worked_off_hours
        elif worked_off_hours > 100:
            monthly_wage += 210*worked_off_hours
        elif worked_off_hours > 80:
            monthly_wage += 160*worked_off_hours
        elif worked_off_hours > 40:
            monthly_wage += 120*worked_off_hours

        total_hours_worked += worked_off_hours
        #total_hours_worked += monthly_hours_worked
        total_wage += monthly_wage

    return total_hours_worked,total_wage