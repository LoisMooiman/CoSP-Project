##################
# Lois Mooiman
# 10318364
#
# Project for Computational Semantics and Pragmatics
# Course 2016-2017, University of Amsterdam
#
# Helpers
##################

#Imports
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

#####################
# HELPERS
#####################

#Change pysrt times to datetime times
def changetime(times):
    hour = times.hours
    minute = times.minutes
    second = times.seconds
    mill = times.milliseconds
    time = dt.time(hour, minute, second, mill)
    return time
    
#Plot
def plottrans(transition_times):
    # compute and plot the mean of all transition times
    mean = np.mean(transition_times)
    plt.axvline(x=mean, ymin=0, ymax=0.9, color='red')
    
    # plot the normalised timing information
    n, bins, patches = plt.hist(transition_times, 5000, histtype='step', normed=True, color='blue')
    #n, bins, patches = plt.hist(transition_times, 5000, normed=True, color='blue')
    plt.axis([-5, 5, 0, 2])
    plt.title("Timing at turn transitions")
    plt.xlabel("Transition time (s)")
    plt.ylabel("Relative Frequency (%)")
    plt.show()       