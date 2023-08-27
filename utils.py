import matplotlib.pyplot as plt

def generate_color(palette_name, num_colors):
    cmap = plt.get_cmap(palette_name)
    hex_colors = ['#%02x%02x%02x' % tuple(int(255 * rgba) for rgba in cmap(i)[:3]) for i in range(num_colors)]
    return hex_colors