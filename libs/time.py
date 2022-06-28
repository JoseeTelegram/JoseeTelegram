def getReadableTime(time: int):
  """ Converts time in seconds to human-readable version. """
  if time < 0: return False

  td = 0
  th = 0
  tm = 0
  ts = 0

  while True:
      if time >= 86400:
          td += 1
          time -= 86400
      elif time >= 3600:
          th += 1
          time -= 3600
      elif time >= 60:
          tm += 1
          time -= 60
      else:
          ts = time
          break
  
  return td, th, tm, ts