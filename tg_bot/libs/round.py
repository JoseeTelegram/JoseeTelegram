import math

def RoundTo(num, digits=2):
  if num == 0: return 0
  scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
  if scale < digits: scale = digits
  return round(num, scale)