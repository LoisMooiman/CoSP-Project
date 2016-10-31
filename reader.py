##################
# Loïs Mooiman
# 10318364
#
# Project for Computational Semantics and Pragmatics
# Course 2016-2017, University of Amsterdam
#
# Reads in relevant files 
##################

#################
# IMPORTS
#################
import numpy as np
import re
import os
import pysrt     #Special import for subtitles
import datetime as dt
import operator
from datetime import datetime
import matplotlib.pyplot as plt
import scipy
from swda_time import CorpusReader

from helpers import changetime, plottrans

#################
# SUBTITLES
#################

# Read in all subtitles:
path = '../Subtitles/'
allsubs = {}
for filename in os.listdir(path):
    filename = os.path.join(path, filename)
    subs = pysrt.open(filename, encoding='iso-8859-1')
    subdict = {}
    i = 0
    for sub in subs:
        if not ( sub.text.startswith('(') and sub.text.endswith(')')) or not ( sub.text.startswith('[') and sub.text.endswith(']')):
            start = changetime(sub.start)
            end = changetime(sub.end)
            if sub.text.endswith('...'):
                laststart = changetime(sub.start)
            elif sub.text.startswith('...'):
                times = (laststart, end)
                subdict[i] = times
                i += 1
            #give the same timestamp if text is said directly after eachother
            elif sub.text.startswith('-'):
                times1 = (start, end)
                subdict[i] = times1
                i += 1
                times2 = (start, end)
                subdict[i] = times2
                i += 1
            else:
                times = (start, end)
                subdict[i] = times
                i += 1
    allsubs[filename] = subdict

print 'COMPUTING TRANSITION TIMES SUBTITLES \n'
#Compute transition times
transition_times = []
j = 0
for filesub in allsubs:
    subdict = allsubs.get(filesub)
    sortedsub = sorted(subdict.items(), key=operator.itemgetter(0))
    lastend = dt.time(0,0,0,0)
    for number in sortedsub:
        time = number[1]
        startT = time[0]
        endT = time[1]
        if lastend == endT:
            transition = 0
            transition_times.append(transition)
            j += 1
        else:
            diff = datetime.combine(dt.date.today(), startT) - datetime.combine(dt.date.today(), lastend)
            transition = diff.total_seconds()
            #Ignore the credits of the subtitles which have weird timing
            if -10< transition < 10:
                transition_times.append(transition)                
    
        lastend = endT

mean = np.mean(transition_times)
var = np.var(transition_times)
std = np.std(transition_times)
print mean
print var
print std

print len(transition_times)

print j

plottrans(transition_times) 

####################
# Switchboard corpus
####################
'''
# import the corpus reader and read in the corpus
corpus = CorpusReader('swda_time', 'swda_time/swda-metadata-ext.csv')
print 'COMPUTING TRANSITION TIMES SWITCHBOARD CORPUS \n'
# iterate over all transcripts in the corpus and compute the turn taking timings
transition_times_corpus = []
for transcript in corpus.iter_transcripts(display_progress=False):
    end_prev_turn = transcript.utterances[0].end_turn
    cur_turn_index = transcript.utterances[0].turn_index
    
    # loop over all utterances
    for utterance in transcript.utterances:
        # check if turn transition took place
        if utterance.turn_index == cur_turn_index:
            end_prev_turn = utterance.end_turn
            continue
        
        # compute transition time
        try:
            transition_time = utterance.start_turn - end_prev_turn
            transition_times_corpus.append(transition_time)
        except TypeError:
            pass
  
        # reset turn index and end of turn
        end_prev_turn, cur_turn_index = utterance.end_turn, utterance.turn_index
        
# print mean and length of transition times  
mean = np.mean(transition_times_corpus)
variance = np.var(transition_times_corpus)
std = np.std(transition_times_corpus)
print mean
print variance
print std
print len(transition_times_corpus)

#Plot
plottrans(transition_times_corpus) 
'''
###################
# DIALOGUE
###################
#TODO:
# Read in file with only actor names
# Match them one to one to the utterances
#Discard small utterances in the subtitles. 

chardict = {}
with open('waterforelephants_dialog.txt', 'r') as dial:
    i = 0
    for line in dial:
        line = line.rstrip()
        if line.strip() and not line.endswith('.') and not line.startswith('(') and not line.endswith('!'):
            words = line.split(' ')
            if len(words) < 2 or words[1].startswith('('):
                chardict[i] = words[0]
                
        i+=1

subs = pysrt.open('waterforelephants_sub.srt', encoding='iso-8859-1')
sub1dict = {}
i = 0
for sub in subs:
    if not ( sub.text.startswith('(') and sub.text.endswith(')')) or not ( sub.text.startswith('[') and sub.text.endswith(']')):
        start = changetime(sub.start)
        end = changetime(sub.end)
        if sub.text.endswith('...'):
            laststart = changetime(sub.start)
        elif sub.text.startswith('...'):
            times = (laststart, end)
            sub1dict[i] = times
            i += 1
        #give the same timestamp if text is said directly after eachother
        elif sub.text.startswith('-'):
            times1 = (start, end)
            sub1dict[i] = times1
            i += 1
            times2 = (start, end)
            sub1dict[i] = times2
            i += 1
        else:
            times = (start, end)
            sub1dict[i] = times
            i += 1

sortedsub = sorted(sub1dict.items(), key=operator.itemgetter(0))
sortedchar = sorted(chardict.items(), key=operator.itemgetter(0))

j = 0
lastspeaker = ''
transition_times = []
for char in sortedchar:
    speaker = char[1]
    sub = sortedsub[j]
    if not speaker == lastspeaker:
        time = sub[1]
        startT = time[0]
        endT = time[1]
        if lastend == endT:
            transition = -0.75
            transition_times.append(transition)
        else:
            diff = datetime.combine(dt.date.today(), startT) - datetime.combine(dt.date.today(), lastend)
            transition = diff.total_seconds()
            #Ignore the credits of the subtitles which have weird timing
            if -60< transition < 60:
                transition_times.append(transition)                
        
        lastend = endT
        j += 1
    lastspeaker = speaker
    
mean = np.mean(transition_times)
var = np.var(transition_times)
std = np.std(transition_times)
print mean
print var
print std

print len(transition_times)


plottrans(transition_times) 



