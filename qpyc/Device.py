import numpy as np
import copy
import matplotlib.pyplot as plt

from qpyc.Visualize import plot_circuit

def checkAddr(addr):
    """
    Check if the address is valid, in the form (x,y) and x+y is even
    """
    if not all(isinstance(i, int) for i in addr) or len(addr) != 2:
        raise TypeError('Wrong address format.')
    # elif sum(addr) % 2 != 0:
        # raise ValueError('The sum of x,y coordinates should be even')
    # else:
        # pass

class Component:
    def __init__(self, addr=None, dom=None) -> None:
        """Optical Component
        A abstract python class of optical components which can be 
        1. added/deleted/modified into Circuir class
        2. estimated by the property 'matrix'
        The Component depth is always 1.

        Parameters
        ----------
        addr : list, optional
            address is like (x, y),
            x is the column index 
            y is the index of first waveguide
            by default None
        dom : int, optional
            component dimension/width
            i.e. the waveguides/input ports/output ports number, by default None
        """
        # check(addr)
        self._addr = addr
        self.dom = dom
        self._matrix = np.array([], dtype=np.complex_)

    def __repr__(self) -> str:
        return f'Component ({self.addr})'

    @property
    def addr(self):
        """Address of Component

        Returns
        -------
        list
            (x, y)
            x is the column index
            y is the index of the first input port
        """
        return self._addr

    @addr.setter
    def addr(self, addr):
        checkAddr(addr)
        self._addr = addr

    @property
    def x(self):
        """x coordinate of Component

        Returns
        -------
        int
            the column index
        """
        return self._addr[0]

    @x.setter
    def x(self, xx):
        assert type(xx) is int
        self._addr[0] = xx

    @property
    def y(self):
        """y coordinate of Component

        Returns
        -------
        int
            the index of the first input port
        """
        return self._addr[1]

    @y.setter
    def y(self, yy):
        assert type(yy) is int
        self._addr[1] = yy

    @property
    def ports(self):
        """Waveguide indices of Component

        Returns
        -------
        list
            waveguide/port indices

        >>> C = Component(addr=[1,2], dom=3)
        >>> C.ports
        [2, 3, 4]
        """
        return list(range(self.y, self.y + self.dom))

    @property
    def matrix(self):
        """Matrix representation

        Returns
        -------
        np.array
            A dom x dom 2D np array
        """
        return self._matrix

    @matrix.setter
    def matrix(self, mat):
        self._matrix = np.array(mat, dtype=np.complex_)

    def merge(self, other):
        """Merge one component with another in series

        Parameters
        ----------
        other : Component
            component to merge with

        Returns
        -------
        Component
            A new Component with current address and product matrix

        Raises
        ------
        TypeError
            A Component can only be merged with another Component
        ValueError
            Only Component with the same dimension can be merged

        >>> C = Component()
        >>> D = Component()
        >>> C.matrix = np.array([[1,2],[3,4]])
        >>> D.matrix = np.diag([1,2])
        >>> E = C.merge(D)
        >>> assert np.allclose( E.matrix, np.array([[1,4],[3,8]]) )
        """
        if isinstance(other, Component) is not True:
            raise TypeError('A Component can only be merged with another Component.')
        elif other.dom != self.dom:
            raise ValueError('Only Component with the same dimension can be merged.')
        comp = Component(addr=self._addr)
        comp.dom = self.dom
        comp.matrix = np.matmul(other.matrix, self.matrix)
        return comp

    def span(self, other):
        """Span one component with another in parallel

        Parameters
        ----------
        other : Component
            component to span with

        Returns
        -------
        Component
            A new Component with current address and product matrix

        Raises
        ------
        TypeError
            A component can only spanned with another Component

        >>> C = Component(dom=2)
        >>> D = Component(dom=2)
        >>> C.matrix = np.diag([3,4])
        >>> D.matrix = np.diag([1,2])
        >>> E = C.span(D)
        >>> assert np.allclose( E.matrix, np.diag([3,4,1,2]) )
        """
        if isinstance(other, Component) is not True:
            raise TypeError
        comp = Component(addr=self._addr)
        comp.dom = self.dom + other.dom
        m = np.zeros((comp.dom, comp.dom), dtype=np.complex_)
        m[:self.dom, :self.dom] = self.matrix
        m[self.dom:, self.dom:] = other.matrix
        comp.matrix = m
        return comp

    def __matmul__(self, other):
        """Use @ symbol to span"""
        return self.span(other)

    def __lshift__(self, other):
        """Use << to merge on the left"""
        return other.merge(self)

    def __rshift__(self, other):
        """Use >> to merge on the right"""
        return self.merge(other)


class Waveguide(Component):
    def __init__(self, dom=1, addr=None) -> None:
        """Optical Waveguide

        Parameters
        ----------
        dom : int, optional
            number of waveguides, by default 1
        addr : list, optional
            address, by default None
        """
        super().__init__(addr, dom)

    def __repr__(self) -> str:
        return f'Waveguide ({self.addr}, Dim={self.dom})'

    @property
    def matrix(self):
        """matrix of Waveguide

        Returns
        -------
        np.array
            A diagonal array

        >>> W = Waveguide(dom=2)
        >>> assert np.allclose(W.matrix, [[1,0],[0,1]])
        """
        return np.eye(self.dom, dtype=np.complex_)


class PhaseShifter(Component):
    def __init__(self, phase=0, addr=None) -> None:
        """Phase shifter

        Parameters
        ----------
        phase : int, optional
            phase in unit of pi, by default 0
        addr : list, optional
            address, by default None
        """
        super().__init__(addr, dom=1)
        self.phase = phase

    def __repr__(self) -> str:
        return f'PhaseShifter({self.addr}, Phase={self.phase})'

    @property
    def matrix(self):
        return np.array([np.exp(1j*self.phase*np.pi)], dtype=np.complex_)

    def dagger(self):
        return PhaseShifter(phase=-self.phase, addr=self.addr)


class BeamSpiliter(Component):
    def __init__(self, bias=0, addr=None) -> None:
        """Beam spiliter with imperfection, with respect to 50:50

        :param bias: bias angle in unit of pi, defaults to 0
        :type bias: int, optional
        :param addr: address, defaults to None
        :type addr: list, optional
        """
        super().__init__(addr, dom=2)
        self.bias = bias

    def __repr__(self):
        return f'BeamSpiliter ({self.addr}, Bias={self.bias})'

    @property
    def matrix(self):
        sin = np.sin((0.25 + self.bias) * np.pi)
        cos = np.cos((0.25 + self.bias) * np.pi)
        return np.array([[sin, 1j * cos], [1j * cos, sin]], dtype=np.complex_)

    def dagger(self):
        """Conjugate transpose of BeamSpiliter by changing the matrix

        Returns
        -------
        BeamSpilier
            Conjugate transpose of BeamSpiliter

        >>> BS = BeamSpiliter(bias=.25)
        >>> BSD = BS.dagger()
        >>> assert np.allclose(np.matmul(BS.matrix, BSD.matrix), np.eye(2))
        """
        dag = BeamSpiliter(bias=self.bias, addr=self.addr)
        dag._matrix = np.conjugate(self.matrix)
        return dag


class MZI(Component):
    def __init__(self, theta=0, phi=0, bias=[0, 0], addr=None) -> None:
        """Mach-Zehnder interferometor consisting of 2 biased beam spilitters and 2 phase shifters.

        Parameters
        ----------
        theta : int, optional
            internal phase, by default 0
        phi : int, optional
            external phase, by default 0
        bias : list, optional
            biases of two beam spiliters, by default [0, 0]
        addr : list, optional
            address, by default None        

        TODO: change the parameters into property

        """
        super().__init__(addr, dom=2)
        self.theta = theta
        self.phi = phi
        self.bias = bias

    def __repr__(self) -> str:
        return f'MZI ({self.addr}, Phase={self.theta}, {self.phi})'

    @property
    def matrix(self):
        """
        TODO: rewrite the matrix representation here
        
        >>> U2 = MZI(phase=.3, phi=.25)
        >>> np.allclose(U2.matrix, )
        """
        mzi = PhaseShifter(self.phi) @ Waveguide() >> BeamSpiliter(self.bias[0]) >> \
            PhaseShifter(
                self.theta) @ Waveguide() >> BeamSpiliter(self.bias[1])
        return mzi.matrix

class Circuit:
    """Cricuit class

    A Circuit instance created by this class is a dynamic object consisting of several devices.
    In principle, all devices should be
    1.  coordinated and not overlapped
    2.  added or removed by objects or coordinates
    Likewise, Circuit can of course be extended in parallel or in series
    """

    def __init__(self) -> None:
        self._devices = []

    def __repr__(self) -> str:
        return [d.__repr__() for d in self._devices]

    @property
    def devices(self):
        """A dictionary including all Circuit devices

        Returns
        -------
        dict
            A dictionary including all Circuit devices, the key is address tuple and the value is Component.
            Note that _devices attribute is list.
        """
        self._devices.sort(key=lambda d: d.y)
        self._devices.sort(key=lambda d: d.x)
        return {tuple(d.addr): d for d in self._devices}
    
    @property
    def addrs(self):
        """All Component address

        >>> C = Circuit()
        >>> C.add(Waveguide(dom=2), Waveguide(dom=3))
        >>> assert C.addrs == [(1,1), (2,1)]
        """
        return list(self.devices.keys())

    @property
    def width(self):
        """
        Circuit width, maximal y coordinate 
        """
        return max([d.y+d.dom for d in self._devices]) if len(self._devices) != 0 else 0

    @property
    def depth(self):
        """
        Circuit depth, maximal x coordinate 
        """
        return max([d.x for d in self._devices]) if len(self._devices) != 0 else 0
    
    def __contains__(self, d):
        """If Device in Circuit.

        Parameters
        ----------
        d : Device

        >>> C = Circuit()
        >>> W = Waveguide()
        >>> C.add(W)
        >>> assert W in C
        
        """
        return d in self._devices

    def __getitem__(self, item):
        """Get Device item in Circuit.

        Parameters
        ----------
        item : tuple
            address of device

        Returns
        -------
        Component
            The Component to return

        >>> C = Circuit()
        >>> C.add(Waveguide(dom=2))
        >>> print(C[(1,1)])
        Waveguide ([1, 1], Dim=2)
        """
        if item in self.addrs:
            return self.devices[item]
        else:
            raise ValueError('Required address has no Component.')

    def __add_single(self, d):
        """_summary_

        Parameters
        ----------
        d : _type_
            _description_

        >>> C = Circuit()
        >>> C.add(Waveguide(dom=2), Waveguide(dom=3))
        >>> assert C.width == 3
        """
        if isinstance(d, Component) is False:
            raise TypeError('Only Component can be added into Circuit.')
        elif d in self._devices:
            raise Warning('Device is already in Circuit.')
        else:
            if d._addr == None:
                d._addr = [self.depth + 1, 1]
            elif d._addr in self.addrs:
                raise Warning(f'Overlap Component at {d.addr}')
            self._devices.append(d)

    def add(self, d, *dd):
        """
        Add devices into the circiut.
        
        >>> C = Circuit()
        >>> C.add(Waveguide(dom=2), Waveguide(dom=3))
        >>> assert C.width == 3
        
        """
        self.__add_single(d)
        if dd is not None:
            [self.__add_single(d) for d in dd]

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
        for d in self._devices:
            assert isinstance(d, Component)
            submat = np.eye(self.width, dtype=np.complex_)
            submat[d.y-1:d.y+d.dom-1, d.y-1:d.y+d.dom-1] = d.matrix
            mat = np.matmul(mat, submat)
        return mat

    def copy(self):
        Circ = Circuit()
        Circ._devices = [copy.deepcopy(d) for d in self._devices]
        return Circ

    def multiple(self, other):
        """
        Multiple Circuit in series.

        >>> C1 = Circuit()
        >>> C1.add(Waveguide(dom=2))
        >>> C2 = Circuit()
        >>> C2.add(MZI(theta=1))
        >>> C3 = C1.multiple(C2)
        >>> print(C3.matrix)
        # >>> assert np.allclose(C3.matrix, [[1,1],[1,1]] )
        """
        if isinstance(other, Circuit) is not True:
            raise TypeError('Circuit can only be merged with Circuit.')
        Circ = Circuit()
        Circ._devices += copy.deepcopy(self._devices)
        other_devices = copy.deepcopy(other._devices)
        for d in other_devices:
            d.x += self.depth
        Circ._devices += other_devices
        return Circ

    def stack(self, other):
        """
        Stack two Circuits in parallel.

        >>> C1 = Circuit()
        >>> C1.add(Waveguide(dom=2))
        >>> C2 = Circuit()
        >>> C2.add(PhaseShifter(phase=0))
        >>> C3 = C1.stack(C2)
        >>> assert np.allclose(C3.matrix, np.diag([1,1,1]))
        """
        if isinstance(other, Circuit) is not True:
            raise TypeError('Circuit can only be merged with Circuit.')
        Circ = Circuit()
        Circ._devices += copy.deepcopy(self._devices)
        other_devices = copy.deepcopy(other._devices)
        for d in other_devices:
            d.y += self.width
        Circ._devices += other_devices
        return Circ

    def __rshift__(self, other):
        return self.multiple(other)

    def __lshift__(self, other):
        return other.multiple(self)

    def __matmul__(self, other):
        return self.stack(other)

    def plot(self):
        _, ax = plt.subplots()
        ax = plot_circuit(self, ax)
        plt.show()
        # plt.close()
