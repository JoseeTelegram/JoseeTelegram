import math
import sys
from PIL import Image, ImageDraw

pad = 50
size = 500
rad = (size - pad) / 2

angles = 6
deg = 360 / angles

img = Image.new("RGB", (size, size), (255, 255, 255))
draw = ImageDraw.Draw(img)

a = []

for i in range(0, angles+1):
  a.append(math.radians(deg*i))

print(a)

for i in range(0, angles):
  line = (
    math.cos(a[i]) * rad + size / 2,
    math.sin(a[i]) * rad + size / 2,
    math.cos(a[i+1]) * rad + size / 2,
    math.sin(a[i+1]) * rad + size / 2,
  )
  draw.line(line, 0, 3)

for i in range(0, angles):
  line = (
    math.cos(a[i]) * rad + size / 2,
    math.sin(a[i]) * rad + size / 2,
    size / 2,
    size / 2,
  )
  draw.line(line, 0, 3)

  # debug
  # print(
  # f'n = {i}',
  # f'a = {deg*i}',
  # f'x = {round(x, 2)}',
  # f'y = {round(y, 2)}\n',
  # sep='\n')

img.show()