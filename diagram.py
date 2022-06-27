import math
from PIL import Image, ImageDraw

from colors import get_rainbow

def graph_circle(values: list[int], names: list[str], size: int, padding: float, width: float):
  summ = sum(values)
  rad = (size - padding) / 2

  diagram = Image.new("RGB", (size, size), (255, 255, 255))
  draw = ImageDraw.Draw(diagram)
  colors = get_rainbow(len(values))
  
  prev = 0
  for i in range(0, len(values)):
    curr = values[i] / summ * 360 + prev
    draw.pieslice((padding, padding, size - padding, size - padding), prev, curr, fill = colors[i], outline = "#000", width = width)

    if names[i]:
      text_pos = math.radians(curr - (curr - prev) / 2)
      draw.text((math.cos(text_pos) * rad / 2 + size / 2, math.sin(text_pos) * rad / 2 + size / 2), names[i], "#000", align = "center") # text in slice
      # draw.text((math.cos(text_pos) * rad + size / 2, math.sin(text_pos) * rad + size / 2), names[i], "#000", align = "center") # text on slice
    
    prev = curr

  return diagram

def example():
  data = {
  "name1": 3,
  "name2": 2,
  "name3": 2,
  "name4": 5,
  "name5": 3,
  }
  graph_circle(list(data.values()), list(data.keys()), 1000, 100, 10).show()

if __name__ == "__main__":
  example()