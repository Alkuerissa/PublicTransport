import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from colorsys import hsv_to_rgb
import numpy as np
df = pd.read_csv('../tramwaje.csv')

df['v'] = np.random.choice(range(0, 80), df.shape[0])


class PlotMap:
    m = None
    layers = []
    data = None
    lon_col = 'Lon'
    lat_col = 'Lat'
    min_c = None
    max_c = None
    fig = None
    color_colname = None

    def __init__(self, service, data, color_colname = None):
        self.fig = plt.figure(figsize=(8, 8))
        self.fig.add_axes([0.05, 0.05, 0.8, 0.9])
        self.m = Basemap(projection='mill', resolution='c', epsg=2180,
                         llcrnrlon=20.84, llcrnrlat=52.09, urcrnrlon=21.28, urcrnrlat=52.37)
        self.m.arcgisimage(service=service, xpixels=1920, verbose=False, zorder=0)
        self.plot([])
        self.data = data
        if color_colname is not None:
            self.color_colname = color_colname
            self.set_minmax_color(color_colname)

    def set_minmax_color(self, color_colname):
        self.min_c = min(self.data.loc[:, color_colname])
        self.max_c = max(self.data.loc[:, color_colname])

    def plot(self, indices, color_colname=None, layer=0, draw=True):
        if len(indices) != 0:
            if self.data is None:
                raise TypeError('Data is none.')
            lon, lat = self.m(self.data.loc[indices, self.lon_col].values, self.data.loc[indices, self.lat_col].values)
            if color_colname is None:
                color_colname = self.color_colname
        else:
            lon, lat = [], []

        if len(self.layers) > layer:  # replace a layer
            h = self.layers[layer]
            h.set_offsets([lon, lat])
            if color_colname is not None:
                if self.min_c is None or self.max_c is None:
                    self.set_minmax_color(color_colname)
                h.set_color(val_to_col(self.data.loc[indices, color_colname], minimum=self.min_c, maximum=self.max_c))
            if draw:
                h.figure.canvas.draw()
        elif layer == len(self.layers):  # add a layer
            h = self.m.scatter(lon, lat, zorder=1)
            self.layers.append(h)
        else:  # raise error to prevent discontinuity
            raise IndexError('Layer can be at most {}'.format(len(self.layers)))
        return self.layers[layer]

    def animate(self, selector_func, title_func, color_colname=None, layer=0):
        def anim_func(i):
            indices = selector_func(self.data, i)
            r = self.plot(indices, color_colname=color_colname, layer=layer, draw=False)
            r.axes.set_title(title_func(self.data, indices, i))
            return r

        anim = animation.FuncAnimation(plt.gcf(), anim_func,
                                       init_func=lambda: self.plot([], layer=layer))
        return anim

    def draw_colorbar(self):
        ax = self.fig.add_axes([0.9, 0.05, 0.05, 0.9])
        colormap = partial_colormap(cm.get_cmap('hsv'), 0, 0.33)
        cb = colorbar.ColorbarBase(ax, cmap=colormap, norm=colors.Normalize(vmin=self.min_c, vmax=self.max_c))
        cb.ax.set_title(self.color_colname)

    def show(self):
        self.draw_colorbar()
        plt.show()


def selector(data, i):
    return list(range(i*100, (i+1)*100))


def titler(data, indices, i):
    return data.loc[indices[0], 'Time']


def val_to_col(column, minimum, maximum):  # 0 to 120 deg hue = red to green color
    return [(*hsv_to_rgb(0, 1, 1), 1) if x < minimum
           else (*hsv_to_rgb(0.33, 1, 1), 1) if x > maximum
           else (*hsv_to_rgb(0.33 * (x - minimum)/(maximum - minimum), 1, 1), 1) for x in column]


def partial_colormap(cmap, min_c, max_c, n=1000):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=min_c, b=max_c),
        cmap(np.linspace(min_c, max_c, n)))
    return new_cmap


pm = PlotMap('World_Street_Map', df, color_colname='v')
anim = pm.animate(selector, titler)
pm.show()
