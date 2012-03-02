import twitter
import json
from matches import MatchStore

def get2012MatchData(status) :
  i = status.text.split()
  match = {}
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


numToFetch = 100
running = True
i=1
curPage = 1
ms = MatchStore('2012')
lastIDFetched = ms.getLatestMatchID()

while running :
  statuses = api.GetUserTimeline("frcfms", since_id=lastIDFetched, count=numToFetch, page=curPage)
  print "Fetched",len(statuses),"matches"
  for s in statuses : 
    m = get2012MatchData(s)
    ms.addMatch(m)
    print s.text
    print i
    i = i + 1

  if len(statuses) < numToFetch :
    running = False
  else :
    curPage += 1

