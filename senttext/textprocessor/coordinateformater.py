import re

class CoordinateFormater():
   def __init__(self):
      self.zero = ['0','0']
   def formatCoordinate(self,coordinate):
      if coordinate != 'None':
         coordinate = re.sub(r"[\',{\[\]\}:]","",coordinate)
         coordinate = re.sub(r"type Point coordinates ","",coordinate)
         coordinate = coordinate.split()
         invert = coordinate[0]
         coordinate[0] = coordinate[1]
         coordinate[1] = invert
         return coordinate
      else:
         return self.zero
