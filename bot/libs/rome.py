# src: https://ru.stackoverflow.com/questions/499269
def getNearestValue(value: int, list: list):
    """ Returns the index of the nearest value in list. """
    list_of_difs = [abs(value - x) for x in list]
    return list_of_difs.index(min(list_of_difs))


def getRome(value: int):
  """ Converts integer in to Roman numerals system. """
  if value < 0: return False

  rome = {
      1:"I",
      5:"V",
      10:"X",
      50:"L",
      100:"C",
      500:"D",
      1000:"M"
  }
  
  near_int = list(rome.keys())[getNearestValue(value, list(rome.keys()))]
  res = rome[near_int]
  value -= near_int
  
  while value > 0:
      for key in rome.keys():
          if value >= key:
              value -= key
              res += rome[key]
  while value < 0:
      for key in rome.keys():
          if abs(value) <= key:
              value += key
              res = rome[key] + res
  return res