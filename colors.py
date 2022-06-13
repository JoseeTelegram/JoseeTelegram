def rgb2hex(r:int, g:int, b:int):
  return "%02x" % r, "%02x" % g, "%02x" % b 

def rgb2hsv(r:int, g:int, b:int):
  r /= 255
  g /= 255
  b /= 255

  M = max(r, g, b)
  m = min(r, g, b)

  diff = M - m

  h = -1
  if (M == m):
    h = 0
  elif (M == r):
    h = (60 * ((g - b) / diff) + 360) % 360
  elif (M == g):
    h = (60 * ((b - r) / diff) + 120) % 360
  elif (M == b):
    h = (60 * ((r - g) / diff) + 240) % 360

  s = 0
  if M != 0:
    s = (diff / M) * 100

  v = M * 100

  return h, s, v

def rgb2cmyk(r:int, g:int, b:int):
  r /= 255
  g /= 255
  b /= 255

  k = 1 - max(r, g, b)

  return (1 - r - k) / (1 - k) * 100, (1 - g - k) / (1 - k) * 100, (1 - b - k) / (1 - k) * 100, k * 100  

# def rgb2lab(r:int, g:int, b:int):

def main():
  rgb = [123, 83, 76]
  
  r = rgb[0]
  g = rgb[1]
  b = rgb[2]

  print(
  f"RGB: {r}, {g}, {b}\n"
  f"HEX: #{''.join(str(i) for i in rgb2hex(r, g, b))}\n"
  f"HSV: {', '.join(str(round(i)) for i in rgb2hsv(r, g, b))}\n"
  f"CMYK: {', '.join(str(round(i)) for i in rgb2cmyk(r, g, b))}\n"
  )

if __name__ == "__main__":
  main()