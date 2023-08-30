import matplotlib.pyplot as plt
import random


def generate_color(palette_name, num_colors):
    cmap = plt.get_cmap(palette_name)
    hex_colors = ['#%02x%02x%02x' % tuple(int(255 * rgba) for rgba in cmap(i)[:3]) for i in range(num_colors)]
    return hex_colors

def generate_color_from_shades(base_color, num_shades):
    shades = []
    red = random.sample(range(150, 250 + 1), num_shades)
    green = random.sample(range(150, 250 + 1), num_shades)
    for i in range(num_shades):

        r = red[i] if base_color=="red" else 0 
        g = green[i] if base_color=="green" else 0  
        b = 0 

        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

        shades.append(hex_color)

    return shades