# By Joely Nelson
# A very simple file demonstrating how to use the code in models.py

import numpy as np
import matplotlib.pyplot as plt
from models import *

def p(i):
    '''
    Returns a string representation of a number in a readable format surrounded by commas.
    NOTE: Is used by none of the functions, just happens to be kind of useful.
    '''
    return "{:,}".format(int(i))


# Example of simulating America:
# Vaccinations begin 419 days after the start of the pandemic. Simulation lasts for 100 days
t, v = simulate_region(total_pop=330222422, 
                    alpha=0.008, 
                    beta=0.27, 
                    eps=0.2,
                    gamma=0.2, 
                    vac_start_day=340, 
                    vac_rate=5e5, 
                    uptake_per=0.7, 
                    num_vac_days=90)   

# this is how to get out each of the individual values
S,E,I,R,D,V = v.T

print("Number dead: ", p(D[-1]))

# plotting
labels = ['Suceptible', 'Exposed', 'Infected', 'Recovered', 'Dead', 'Vaccinated']
for item, label in zip(v.T, labels):
    plt.plot(t, item, label=label)
plt.axvline(x=340, color='black', alpha=0.5, linestyle='dashed')
plt.legend(loc='best')
plt.show()
plt.clf()