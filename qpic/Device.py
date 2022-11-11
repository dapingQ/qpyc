import numpy as np

class Component:
    """
    Parent class of basic components in a mesh.
    """

    def _check(addr):
        if not all(isinstance(i, int) for i in addr) or len(addr) != 2:
            raise TypeError('Wrong Address.')

    def __init__(self, addr=None, dom=None ) -> None:
        self._addr = addr
        self.dom = dom
        self._matrix = np.array([], dtype=np.complex_)
        # self.matrix = np.eye(self.dom, dtype=np.complex_)
    
    def __repr__(self) -> str:
        return 'Component ()' if self._addr is None else f'Component ({self.addr})'

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, addr):
        self._check(addr)
        self._addr = addr
    
    @property
    def x(self):
        return self._addr[0]
    
    @x.setter
    def x(self, xx):
        assert xx is int 
        self._addr[0] = xx
    
    @property
    def y(self):
        return self._addr[1]
    
    @y.setter
    def y(self, yy):
        assert yy is int
        self._addr[1] = yy
    
    @property
    def matrix(self):
        return self._matrix
    
    @matrix.setter
    def matrix(self, mat):
        self._matrix = mat
    
    def merge(self, other):
        if isinstance(other, Component) is not True:
            raise TypeError('Use component')
        elif other.dom != self.dom:
            raise TypeError('Wrong dimension to merge')
        comp = Component()
        comp.dom = self.dom
        comp.matrix = np.matmul(self.matrix, other.matrix)
        return comp

    def __matmul__(self, other):
        if isinstance(other, Component) is not True:
            raise TypeError
        comp = Component()
        comp.dom = self.dom + other.dom
        m = np.zeros((comp.dom, comp.dom), dtype=np.complex_)
        m[:self.dom, :self.dom] = self.matrix
        m[self.dom:, self.dom:] = other.matrix
        comp.matrix = m
        return comp

    def __lshift__(self, other):
        return other.merge(self)
    
    def __rshift__(self, other):
        return self.merge(other)

    
    @property
    def clements_addr(self):
        """
        Neboughoring waveguide numbers used in Clements coding to decompese the SU(N) into the sub SU(2) matrix.
        """
        return (self.y, self.y + 1)

    @property
    def clements_index(self):
        """
        Index using the clements coding, in the diagonal order.
        """
        return int( sum(self.addr)**2*.25 - self.addr[1] )
        
class Waveguide(Component):
    def __init__(self, dom=1, addr = None) -> None:
        super().__init__(addr, dom)
    
    def __repr__(self) -> str:
        return f'Waveguide ({self.dom})'
    
    @property
    def matrix(self):
        return np.eye(self.dom, dtype=np.complex_)


class PhaseShifter(Component):
    def __init__(self, phase = 0, addr = None) -> None:
        super().__init__(addr, dom=1)
        self.phase = phase
        
    def __repr__(self) -> str:
        return f'PhaseShifter({self.phase})'

    @property
    def matrix(self):
        return np.array([np.exp(1j*self.phase*np.pi)], dtype=np.complex_)

    def dagger(self):
        return np.array([np.exp(-1j*self.phase*np.pi)])

class BeamSpiliter(Component):
    def __init__(self, bias = 0, addr = None) -> None:
        super().__init__(addr, dom=2)
        self.bias = bias
    
    def __repr__(self):
        return f'BeamSpiliter (Bias:{self.bias})'

    @property
    def matrix(self):
        sin = np.sin((0.25 + self.bias) * np.pi)
        cos = np.cos((0.25 + self.bias) * np.pi)
        return np.array([[sin, 1j * cos], [1j * cos, sin]])

class MZI(Component):
    """
    Mach-Zehnder interferometor consisting of 2 biased beam spilitters and 2 phase shifters.
    """
    def __init__(self, theta, phi, bias = [0,0], addr = None) -> None:
        super().__init__(addr, dom=2)
        self.theta = theta
        self.phi = phi
        self.bias = bias

    def __repr__(self) -> str:
        return f'MZI ({self.theta}, {self.phi})'

    @property
    def matrix(self):
        mzi = PhaseShifter(self.phi) @ Waveguide() >> BeamSpiliter(self.bias[0]) >> \
            PhaseShifter(self.theta) @ Waveguide() >> BeamSpiliter(self.bias[1])
        return mzi.matrix

class Circuit:
    """
    Circuit class
    """
    def __init__(self) -> None:
        # self.dim = 2
        self._devices = []

    def __repr__(self) -> str:
        return [d.__repr__() for d in self._devices]

    @property
    def width(self):
        """
        Circuit width, maximal y coordinate + 2
        """
        return max([ d.y for d in self._devices ]) + 2
    
    @property
    def depth(self):
        """
        Circuit depth, maximal x coordinate + 1
        """
        return max([ d.x for d in self._devices ]) + 1
        
    @property
    def devices(self):
        self._devices.sort(key = lambda d: d.x)
        return self._devices

    @property
    def dev_addr(self):
        return [d.addr for d in self._devices]

    @devices.setter
    def devices(self, dd):
        self._devices = dd
        
    def add(self, *dd):
        """
        Add devices into the circiut.
        """
        for d in dd:
            assert isinstance(d , Component) and (d not in self._devices)
            self._devices.append(d)

    def remove(self, device):
        """
        Remove single device by device obejct.
        To do: by coordinate
        """
        assert device in self._devices
        self._devices.remove(device)

    @property
    def matrix(self):
        """
        Calculate the circuit matrix.
        To do: split the devices by columns
        """
        mat = np.eye(self.width)
        for d in self.devices:
            assert isinstance(d, Component)
            submat = np.eye(self.width)
            submat[d.y:d.y+2,d.y:d.y+2] = d.matrix
            mat = mat@submat
        return mat

    def __matmul__(self, other):
        """
        Multiple Circuit in series
        """
        assert isinstance(other, Circuit)
        C = Circuit()
        C.devices += self.devices
        for d in other.devices:
            d.x += self.width
        C.devices += other.devices
        return C

    def __rshift__(self, other):
        if isinstance(other, Component):
            self.add(other)
        elif isinstance(other, Circuit):
            C = Circuit()
            C.devices += self.devices
            for d in other.devices:
                d.x += self.width
            C.devices += other.devices
            return C

    # def __rshift__(self, other):


