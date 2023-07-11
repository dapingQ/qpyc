import numpy as np
from qpyc.Device import Circuit, MZI


# ╔════════╦════════╦════════╦════════╦════════╦════════╗
# ║ (1,1)  ║        ║ (3,1)  ║        ║ (5,1)  ║        ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║        ║ (2,2)  ║        ║ (4,2)  ║        ║ (6,2)  ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║ (1,3)  ║        ║ (3,3)  ║        ║ (5,3)  ║        ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║        ║ (2,4)  ║        ║ (4,4)  ║        ║ (6,4)  ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║ (1,5)  ║        ║ (3,5)  ║        ║ (5,5)  ║        ║
# ╚════════╩════════╩════════╩════════╩════════╩════════╝

    
class ClementsMZI(MZI):
    def __init__(self, 
                 theta=0,
                 phi=0, 
                 bias=..., 
                 addr=None,
                 ext_co = [0,0,0]) -> None:
        super().__init__(theta, phi, bias, addr)
        self.orientation = ext_co
    
    @property
    def matrix(self):
        ps_mat = []
        mat = np.array([
            [np.exp(np.j*self.phi)*np.cos(self.theta),   np.sin(self.theta)],
            [np.exp(np.j*self.phi)*np.sin(self.theta),   np.cos(self.theta)], 
            ], dtype=np.complex_)
        # return super().matrix
        return mat

    # @property
    # def clements_index(self):
    #     """
    #     Index using the clements coding, in the diagonal order.
    #     """
    #     return int(sum(self._addr)**2*.25 - self.y)

class ClementsMesh(Circuit):
    """Clemenets Mesh 

    Clements, William R., et al. "Optimal design for universal multiport interferometers." Optica 3.12 (2016): 1460-1465.

    Note the definition of 2x2 unitary is different from the original matrix.
    In this package, it is defined as

    exp(j*phi)*cos(theta)   sin(theta)
    exp(j*phi)*sin(theta)   cos(theta)

    Parameters
    ----------
    Circuit : _type_
        _description_
    """
    def __init__(self, dimension=2) -> None:
        super().__init__()
        self.dimension = dimension
        for xx in range(self.dimension):
            for yy in range(xx%2, self.dimension-1, 2):
                self.add(ClementsMZI(addr=[xx, yy]))
        self.N = self.width

    def clements_idx(self, addr):
        """
        Convert the xy coordinates into the index using in clements coding, in the diagonal order.
        """
        return int(sum(addr)**2*.25 - addr[1] )

    def order(self, addr):
        """
        Convert the xy coordinates into the index in the vertical order.
        """
        # checkAddr(addr)
        x, y = addr
        return int( ((x-1)*(self.N-1) + (y-1))//2 )

    # def 

    def Route(self, dev_addr):
        """
        Route the output port for a given phaseshifter
        """
        assert tuple(dev_addr) in self.addrs

        xx = range(self.N)
        
        # plot two guiding function
        y1 = [ x - dev_addr[0] + dev_addr[1] for x in range(self.N) ]
        y2 = [ -x + dev_addr[0] + dev_addr[1] for x in range(self.N) ]
        
        # get two parametric func
        y1 = [ -2 - y if y <-1 else 2*self.N - y if y > self.N else y for y in y1]
        y2 = [ -2 - y if y <-1 else 2*self.N - y if y > self.N else y for y in y2] 
        
        # reflect the func 
        r1 = [(x,y) if y != self.N and y!= -1 else None for x,y in zip(xx, y1)]
        r2 = [(x,y) if y != self.N and y!= -1 else None for x,y in zip(xx, y2)]

        # determine orientation
        port_in = [ y[0] if y[1] - y[0] == 1 else y[0] + 1 for y in [y1, y2]]
        port_out = [ y[-1] + 1 if y[-1] - y[-2] == 1 else y[-1]  for y in [y1, y2]]
        
        # yielf waveguide number to avoid N and -1
        port_in = [ self.N-1 if i == self.N else 0 if i == -1 else i for i in port_in]
        port_out = [ self.N-1 if i == self.N else 0 if i == -1 else i for i in port_out]
        
        return r1, r2, port_in, port_out
    
    def RouteExt(self, addr):
        pass


class Sweep(object):
    def __init__(self) -> None:
        pass