import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation

df = pd.read_csv('../tramwaje.csv')


class PlotMap:
    m = None
    layers = []
    data = None
    lon_col = 'Lon'
    lat_col = 'Lat'

    def __init__(self, service, data):
        self.m = Basemap(projection='mill', resolution='c', epsg=2180,
                         llcrnrlon=20.84, llcrnrlat=52.09, urcrnrlon=21.28, urcrnrlat=52.37)
        self.m.arcgisimage(service=service, xpixels=1920, verbose=False)
        self.plot([])
        self.data = data

    def plot(self, data_slice, c=None, layer=0, draw=True):
        if len(data_slice) != 0:
            if self.data is None:
                raise TypeError('Data is none.')
            lon, lat = self.m(self.data.loc[data_slice, self.lon_col].values, self.data.loc[data_slice, self.lat_col].values)
        else:
            lon, lat = [], []

        if len(self.layers) > layer:  # replace a layer
            h = self.layers[layer]
            h.set_data(lon, lat)
            if c is not None:
                h.set_c(c)
            if draw:
                h.figure.canvas.draw()
        elif layer == len(self.layers):  # add a layer
            h, = self.m.plot(lon, lat, 'o')
            self.layers.append(h)
        else:  # raise error to prevent discontinuity
            raise IndexError('Layer can be at most {}'.format(len(self.layers)))
        return self.layers[layer]

    def animate(self, selector_func, title_func, layer=0):
        def anim_func(i):
            slice = selector_func(self.data, i)
            r = self.plot(slice, layer=layer, draw=False)
            r.axes.set_title(title_func(self.data, slice))
            return r

        anim = animation.FuncAnimation(plt.gcf(), anim_func,
                                       init_func= lambda: self.plot([], layer=layer))
        return anim


def selector(data, i):
    return list(range(i*100, (i+1)*100))


def titler(data, slice):
    return data.loc[slice[0], 'Time']


plt.figure(figsize=(8, 8))
pm = PlotMap('World_Street_Map', df)
pm.plot(list(range(100, 201)))
anim = pm.animate(selector, titler)
plt.show()
