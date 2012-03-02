import pymongo

class MatchStore:
  firstID = 0

  def __init__(self, year='2012'):
    self.conn = pymongo.Connection()
    db = 'fms'# + year
    self.matches = self.conn[db].matches

  def getLatestMatchID(self):
    for m in self.matches.find().sort("t_id", pymongo.DESCENDING).limit(1):
      return m['t_id']
    return self.firstID
  
  def addMatch(self, match):
    self.matches.save(match)
