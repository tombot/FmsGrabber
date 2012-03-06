import twitter
import json
from matchstore import MatchStore

min2012 = 158306092244418561 # First meaningful tweet in 2012
max2011 = 132877548332924929 # Last meaningful tweet in 2011

def get2012MatchData(status) :
  i = status.text.split()
  match = {}
  match['year'] = 2012
  match['event'] = i[0][4:]
  match['type'] = i[2]
  match['number'] = int(i[4])
  match['red_final'] = int(i[6])
  match['blue_final'] = int(i[8])
  red_teams = [ int(i[10]), int(i[11]), int(i[12]) ]
  match['red_alliance'] = red_teams
  blue_teams = [ int(i[14]), int(i[15]), int(i[16]) ]
  match['blue_alliance'] = blue_teams
  match['red_bonus'] = int(i[18])
  match['blue_bonus'] = int(i[20])
  match['red_fouls'] = int(i[22])
  match['blue_fouls'] = int(i[24])
  match['red_hybrid'] = int(i[26])
  match['blue_hybrid'] = int(i[28])
  match['red_teleop'] = int(i[30])
  match['blue_teleop'] = int(i[32])
  match['coopertition'] = int(i[34])
  match['t_id'] = s.id
  match['date'] = s.created_at
  return match 

def get2011MatchData(status) :
  i = status.text.split()
  match = {}
  match['year'] = 2011
  match['event'] = i[0][4:]
  match['type'] = i[2]
  match['number'] = int(i[4])
  match['red_final'] = int(i[6])
  match['blue_final'] = int(i[8])
  red_teams = [ int(i[10]), int(i[11]), int(i[12]) ]
  match['red_alliance'] = red_teams
  blue_teams = [ int(i[14]), int(i[15]), int(i[16]) ]
  match['blue_alliance'] = blue_teams
  match['red_bonus'] = int(i[18])
  match['blue_bonus'] = int(i[20])
  match['red_fouls'] = int(i[22])
  match['blue_fouls'] = int(i[24])
  match['t_id'] = s.id
  match['date'] = s.created_at
  return match 

api = twitter.Api()
ms = MatchStore()

running = True
pageLength = 100
i=0
curPage = 1

lastIDFetched = ms.getLatestMatchID()
print "Starting to fetch from Tweet ID: ", lastIDFetched

while running :
  statuses = api.GetUserTimeline("frcfms", since_id=lastIDFetched, count=pageLength, page=curPage)
  for s in statuses : 
    if s.id > min2012:
      m = get2012MatchData(s)
      ms.addMatch(m)
    elif s.id < max2011:
      m = get2011MatchData(s)  
      ms.addMatch(m)
    r =  s.text.split()
    print i, r[0], r[2], r[4]
    i = i + 1

  if len(statuses) < pageLength :
    running = False
  else :
    curPage += 1

print "Fetched", i ,"matches"
