#   
#   
#   Relocation of old code from main.py
#   
#   

from classes.helpers.timer import Timer

sum = Timer.measure(sum)
sum([1,2,3,4])

Timer.report()