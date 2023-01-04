import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# from qpic.Device import Circuit

# single device 
DX = 8
DY = 8
LX = 10
LY = 10

# arguments of genenral circuits
ARGS = {
    'width': DX,
    'linewidth': 1, # linewidth of rect
    'edgecolor': 'black', # edge color of rect
    'facecolor': 'white', # facecolor of rect
    'zorder': 2
}


def plot_circ(Circ, ax):
    """Plot Circuit object at a grid.
    As each Component the depth is always 1, it is poloted as a vertical rectangular.

    Parameters
    ----------
    Circ : Circuit
        Circuit object
    ax : matplotlib.Axes
        The Axes to plot

    Returns
    -------
    matplotlib.Axes
        A plotted Axes with all elements
    """
    # assert type(Circ) is Circuit
    WIDTH = Circ.depth * LX
    HEIGTH = Circ.width * LY 

    [ ax.plot([0,WIDTH+LX+DX], [y,y], 'black', zorder=0) for y in np.arange(0, HEIGTH, LY)+LY+DY*.5 ]
    [ ax.add_patch( patches.Rectangle((d.x*LX, d.y*LY ), height=(d.dom-1)*LY+DY, **ARGS) ) for d in Circ._devices ]
    
    # [ ax.text( d.x*LX+DX*.5, d.y*LY+DY*.5, d.__class__.__name__+str(d.addr), horizontalalignment='center', \
            # verticalalignment='center', transform=ax.transAxes) for d in Circ._devices ]
    [ ax.text( d.x*LX+DX*.5, d.y*LY+DY*.5, d.__class__.__name__+str(d.addr), rotation='vertical') for d in Circ._devices ]
    ax.axis('off')
    return ax