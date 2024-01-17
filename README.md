I made a program with tkinter for the local Burger King employees to calculate their income.

The program has to consider a few criteria in order to work.
  1. Bonuses based on time:
     -Weekend bonus -> 10%
     -Shift allowance -> 30% after 6pm, 40% after 10pm
     
  2. Breaks
     -If they work work >6 hours a day they have a 20 minutes long break
     -But on the wage paper these breaks are actually considered 30 miuntes long and they get paid like they went to break after the 2nd workhour
     -The payment itself complicates things more. For example if the 2nd work hour is between 5pm-6pm than the next 0.5 hour (break) is not getting the shift allowance bonus (here 30%)
     
  3. Bonus after how many hours worked in the month
     -It is based on the actually worked off hours -> breaks don't count in
