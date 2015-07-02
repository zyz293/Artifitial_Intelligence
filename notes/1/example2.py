#
#  change.py, a program to calculate the value of
#             some change in dollars
#

def change():
    print "Change Counter"
    print
    print "Please enter the count of each coin type."
    quarters = int(raw_input("Quarters: "))
    dimes = int(raw_input("Dimes: "))
    nickels = int(raw_input("Nickels: "))
    pennies = int(raw_input("Pennies: "))
    total = quarters * 0.25 + dimes * 0.10 + nickels * 0.05 + pennies * 0.01
    print
    print "The total value of your change is", total

change()
