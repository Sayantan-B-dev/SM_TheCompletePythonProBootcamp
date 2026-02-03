# extract_colors.py
import colorgram

colors = colorgram.extract('136_image.jpg', 10)

rgb_colors = [(c.rgb.r, c.rgb.g, c.rgb.b) for c in colors]

with open('palette.py', 'w') as f:
    f.write("RGB_COLORS = " + str(rgb_colors))
