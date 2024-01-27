import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# from qpyc.Device import Circuit

# single grid size 
DX = 8
DY = 8
# lattice size
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


def plot(Circ, ax):
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

    [ ax.plot([-LX+DX, WIDTH+LX], [y, y], 'black', zorder=0) for y in np.arange(0, HEIGTH, LY)+LY ]
    [ ax.add_patch( patches.Rectangle((d.x*LX, HEIGTH-d.y*LY-d.dom*.5*LY-.5*DY ), height=(d.dom-1)*LY+DY, **ARGS) ) for d in Circ._devices ]    
    # [ ax.text( d.x*LX+DX*.5, HEIGTH-d.y*LY-d.dom*.5*LY+.5*DY, str(d.addr), rotation='vertical', verticalalignment='center', horizontalalignment='center'
            #   ) for d in Circ._devices ]

    [ ax.text(-LX+DX-5, HEIGTH-LY*y, str(y)) for y in range(Circ.width)]
    [ ax.text(WIDTH+LX+4, HEIGTH-LY*y, str(y)) for y in range(Circ.width)]
    
    ax.axis('off')
    return ax

def plot_address(Circ, ax):
    WIDTH = Circ.depth * LX
    HEIGTH = Circ.width * LY 
    _ax = plot(Circ, ax)
    [ _ax.text( d.x*LX+DX*.5, HEIGTH-d.y*LY-d.dom*.5*LY+.5*DY, str(d.addr), rotation='vertical', verticalalignment='center', horizontalalignment='center'
              ) for d in Circ._devices ]
    return _ax

def plot_phase(Mesh, ax):
    WIDTH = Mesh.depth * LX
    HEIGTH = Mesh.width * LY 
    _ax = plot(Mesh, ax)
    [ _ax.text( d.x*LX+DX*.5, HEIGTH-d.y*LY-d.dom*.5*LY+.5*DY, str(d.phase), rotation='vertical', verticalalignment='center', horizontalalignment='center'
              ) for d in Mesh._devices ]
    return _ax

def plot_light(Mesh, route, ax):
    # todo
    return None