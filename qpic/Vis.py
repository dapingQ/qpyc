import matplotlib.pyplot as plt
import matplotlib.patches as patches
from qpic.Mesh import ClementsMesh
from qpic import Component
import numpy as np

MESH = ClementsMesh(6)
# MESH.add(Component((3,4), dom=3))
print(MESH.dev_addr)
DX = 8
DY = 8
LX = 10
LY = 10
ARGS = {
    # 'height': DY,
    'width': DX,
    'linewidth': 1, 
    'edgecolor': 'black',
    # 'color': 'white',
    'facecolor': 'white',
    # 'fill': True
    'zorder': 2

}

WIDTH = MESH.depth * LX
HEIGTH = MESH.width * LY 

fig, ax = plt.subplots()
[ ax.plot([0,WIDTH+LX+DX], [y,y], 'black', zorder=0) for y in np.arange(0, HEIGTH, LY)+LY+DY*.5 ]
# ax.hlines( xmax=WIDTH+LX+DX, xmin=0, y=np.arange(0, HEIGTH, LY)+LY+DY*.5 )
# Create a Rectangle patch


[ ax.add_patch( patches.Rectangle((d.x*LX, d.y*LY ), height=(d.dom-1)*LY+DY, **ARGS) ) for d in MESH._devices ]
# [ ax.text( d.x*LX+DX*.5, d.y*LY+DY*.5, d.__class__.__name__+str(d.addr), horizontalalignment='center', \
        # verticalalignment='center', transform=ax.transAxes) for d in MESH._devices ]
[ ax.text( d.x*LX+DX*.5, d.y*LY+DY*.5, d.__class__.__name__+str(d.addr), rotation='vertical') for d in MESH._devices ]


ax.axis('off')

# [ ax.scatter( x=d.x*LX, y= d.y*LY) for d in MESH._devices]


plt.show()