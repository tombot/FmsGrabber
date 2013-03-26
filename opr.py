import scipy
from scipy import linalg, mat
import numpy
import pymongo
import datetime
import argparse
import sys



# Find a value in a list
def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f == item: 
      return item
  return None

def getMatchset(event, year):
  fms_part = "fms"
  if event == "all":
    matchset = conn[fms_part].matches.find({ "year":int(year)})
  else:
    matchset = conn[fms_part].matches.find({ "year":int(year), "event":event})
  return matchset

def findOPR(type, event, year):
  teams = []
  numTeams = 0
  ids = {}
  matches = 0;

  for m in getMatchset(event, year):
    if m['type'] != "Q":
      continue
    matches += 1
    red = m['red_alliance']
    blue = m['blue_alliance']
    for i in range(0,6):
      t =  red[i] if i < 3 else  blue[i-3]
      if find(t, teams) == None:
        teams.append(t)
        ids[t] = numTeams
        numTeams += 1

  if matches < 1 :
    print "no matches found for event:", event
    exit()

  # placeholders for matrices
  A = scipy.zeros((2 * matches, numTeams), int)
  scores = scipy.zeros((2*matches, 1),int)

  # Build 'A' Matrix
  row = 0
  for m in getMatchset(event, year):
    if m['type'] != "Q":
      continue
    blue = m['blue_alliance']
    red = m['red_alliance']
    
    if type == "adjusted" or type == "scalescore":
      rf = m['red_final'] - m['red_climb'] - m['blue_fouls']
      bf = m['blue_final'] - m['blue_climb'] - m['red_fouls']
      if type == "scalescore" and year == "2102":
        rf += m['coopertition'] * 5
        bf += m['coopertition'] * 5
    else :
      rf = m['red_' + type]   
      bf = m['blue_' + type]
    A[row, ids[red[0]]] = 1
    A[row, ids[red[1]]] = 1
    A[row, ids[red[2]]] = 1
    scores[row] = rf
    row += 1
    A[row, ids[blue[0]]] = 1
    A[row, ids[blue[1]]] = 1
    A[row, ids[blue[2]]] = 1
    scores[row] = bf
    row += 1

  # Find OPR
  Y = mat(A)
  S = mat(scores)
  O = Y.I*S

  oprs = {}
  i = 0
  for t in teams:
    opr = float(numpy.take(O,[i]))
    oprs[str(t)] = opr
    i += 1

  # Uncomment these to write OPRs to db
  #entry = {"year":int(year), "event":event, "matches": matches, "teams": numTeams, "date":datetime.datetime.now(), "opr":oprs}
  #conn[fms_part].oprs.save(entry)

  order =  sorted(oprs.iteritems(), key=lambda (k,v): (v, k))

  ret = []
  for i in range(len(order)-1, 0, -1):
    ret.append([ order[i][0],order[i][1]])
  return ret


# MAIN
if len(sys.argv) <  2:
  print "Give event short code"
  exit()

event = sys.argv[1]
conn = pymongo.Connection()

if len(sys.argv) < 3:
  year="2013"
else : 
  year=sys.argv[2]

for t in ['final', 'auto', 'teleop', 'fouls', 'climb', 'adjusted', 'scalescore']:
  filename = "out/" + year + "_" + event + "-" + t + ".csv"
  print "Finding", t, "OPR score :", filename
  oprs = findOPR(t, event, year)
  i = 0
  f = open(filename, "w")
  for opr in oprs:
    i += 1
    line = str(i) + ", " +  str(opr[0]) + ", " + str(opr[1]) + "\n"
    f.write(line)
  f.close()



