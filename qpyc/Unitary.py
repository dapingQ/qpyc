from qpyc.Device import Circuit, MZI
import numpy as np
from math import factorial

from jax import jit

def p2s(pat, width):
    '''
    Convert pattern number to state.
    eg [3,4] width 6 <=> [0,0,1,1,0,0]
    '''
    assert max(pat) <= width
    return [pat.count(i) for i in range(width)]


def s2p(state):
    '''
    Convert state tp pattern number.
    eg [0,0,1,1,0,0] <=> [3,4] width 6  
    '''
    ll = [[i]*state[i] for i in range(len(state)) if state[i] != 0]
    return [i for l in ll for i in l]

@jit
def nnperm(M):
    """
    Numpy code for computing the permanent of a matrix,
    from https://github.com/scipy/scipy/issues/7151.
    """
    n = M.shape[0]
    d = np.ones(n)
    j = 0
    s = 1
    f = np.arange(n)
    v = M.sum(axis=0)
    p = np.prod(v)
    while (j < n - 1):
        v -= 2 * d[j] * M[j]
        d[j] = -d[j]
        s = -s
        prod = np.prod(v)
        p += s * prod
        f[0] = 0
        f[j] = f[j + 1]
        f[j + 1] = j + 1
        j = f[0]
    return p / 2 ** (n - 1)

def samp(mat, x, y):
    assert sum(x) == sum(y)
    matrix = mat[s2p(x)][:, s2p(y)]
    divisor = np.sqrt(np.prod([factorial(n) for n in x + y]))
    return nnperm(matrix) / divisor

class Interferometer(object):
    """
    This class defines an interferometer. An interferometer contains an ordered list of variable beam splitters,
    represented here by BS_list. For BS in BS_list, BS[0] and BS[1] correspond to the labels of the two modes
    being interfered (which start at 1). The beam splitters implement the optical transformation defined in equation 1 of:
    Clements, William R., et al. "Optimal design for universal multiport interferometers." Optica 3.12 (2016): 1460-1465.
    This transformation is parametrized by BS[2] (theta) which determines the beam splitter reflectivity, and by BS[3] (phi).
    The interferometer also contains a list of output phases described by output_phases.
    """
    
    def __init__(self, ext='right'):
        assert ext in ['right', 'left']
        self.BS_list = []
        self.output_phases = []
        self.ext = ext
        
    def add_BS(self,BS):
        """Use this to manually add a beam splitter at the output of the current interferometer"""
        self.BS_list.append(BS)
        
    def add_phase(self,phase):    
        """Use this to manually add a phase shift to a selected mode at the output of the interferometer"""
        while phase[0] > np.size(self.output_phases) :
            self.output_phases.append(0)
        self.output_phases[phase[0]-1] = phase[1]
    
    def n_modes(self):          
        """Calculate number of modes involved in the transformation. 
        This is required for unitary_transformation and draw_interferometer"""
        list_modes = []
        for BS in self.BS_list:
            list_modes.append([BS[0],BS[1]])
        return np.max(list_modes)

    
    def unitary_transformation_right(self):       
        """Calculate unitary matrix describing the transformation implemented by the interferometer"""
        N = int(self.n_modes())
        U = np.eye(N,dtype=np.complex_)
        for BS in self.BS_list:
            T = np.eye(N,dtype=np.complex_)
            T[BS[0]-1,BS[0]-1] = np.exp(1j*BS[3])*np.sin(BS[2])
            T[BS[0]-1,BS[1]-1] = np.exp(1j*BS[3])*np.cos(BS[2])
            T[BS[1]-1,BS[0]-1] = np.cos(BS[2])
            T[BS[1]-1,BS[1]-1] = -np.sin(BS[2])
            U = np.matmul(U,T)
        while np.size(self.output_phases) < N:      #Autofill for users who don't want to bother with output phases
            self.output_phases.append(0)
        D = np.diag(np.exp([1j*i for i in self.output_phases]))
        U = np.matmul(U,D)           
        return U

def square_decomposition_right(U):
    """
    This code implements the decomposition algorithm in:
    Clements, William R., et al. "Optimal design for universal multiport interferometers." Optica 3.12 (2016): 1460-1465.
    Note here the 2x2 unitary is different from the one in paper, which is defined as 
    [np.exp(1j*phi)*np.sin(theta),  np.exp(1j*phi)*np.cos(theta)
     np.cos(theta),                 -np.sin(theta)              ]
    """
    N = int(np.sqrt(U.size))
    right_T = []
    BS_list = []
    for ii in range(N-1):
        if np.mod(ii,2) == 0:
            # left
            for jj in range(ii+1):
                modes = [ii-jj+1,ii+2-jj]
                try:
                    theta = np.arctan(np.abs(U[ii-jj+1,N-jj-1]/U[ii-jj,N-jj-1]))
                except:
                    theta = np.pi/2
                try:
                    phi = -np.angle(-U[ii-jj+1,N-jj-1]/U[ii-jj,N-jj-1])
                except:
                    phi = 0
                invT = np.eye(N,dtype=np.complex_)
                invT[modes[0]-1,modes[0]-1] = np.exp(-1j*phi)*np.sin(theta)
                invT[modes[0]-1,modes[1]-1] = np.cos(theta)
                invT[modes[1]-1,modes[0]-1] = np.exp(-1j*phi)*np.cos(theta)
                invT[modes[1]-1,modes[1]-1] = -np.sin(theta)
                U = np.matmul(invT,U)
                BS_list.append([modes[0],modes[1],theta,phi])
        else:
            # right
            for jj in range(ii+1):
                modes = [N+jj-ii-1,N+jj-ii]
                try:
                    theta = np.arctan(np.abs(U[jj,N-ii+jj-2]/U[jj,N-ii+jj-1]))
                except:
                    theta = np.pi/2
                try:
                    phi = -np.angle(U[jj,N-ii+jj-2]/U[jj,N-ii+jj-1])
                except:
                    phi = 0
                T = np.eye(N,dtype=np.complex_)
                T[modes[0]-1,modes[0]-1] = np.exp(1j*phi)*np.sin(theta)
                T[modes[0]-1,modes[1]-1] = np.exp(1j*phi)*np.cos(theta)
                T[modes[1]-1,modes[0]-1] = np.cos(theta)
                T[modes[1]-1,modes[1]-1] = -np.sin(theta)
                U = np.matmul(U,T)
                right_T.append([modes[0],modes[1],theta,phi])
    for BS in np.flip(right_T,0):
        modes = [int(BS[0]),int(BS[1])]
        invT = np.eye(N,dtype=np.complex_)
        invT[modes[0]-1,modes[0]-1] = np.exp(-1j*BS[3])*np.sin(BS[2])
        invT[modes[0]-1,modes[1]-1] = np.cos(BS[2])
        invT[modes[1]-1,modes[0]-1] = np.exp(-1j*BS[3])*np.cos(BS[2])
        invT[modes[1]-1,modes[1]-1] = -np.sin(BS[2])
        U = np.matmul(U,invT)
        theta = np.arctan(np.abs(U[modes[0]-1,modes[0]-1]/U[modes[1]-1,modes[0]-1]))
        phi = np.angle(U[modes[0]-1,modes[0]-1]/U[modes[1]-1,modes[0]-1])        
        invT[modes[0]-1,modes[0]-1] = np.exp(-1j*phi)*np.sin(theta)
        invT[modes[0]-1,modes[1]-1] = np.cos(theta)
        invT[modes[1]-1,modes[0]-1] = np.exp(-1j*phi)*np.cos(theta)
        invT[modes[1]-1,modes[1]-1] = -np.sin(theta)
        U = np.matmul(invT,U)
        BS_list.append([modes[0],modes[1],theta,phi])
    phases = np.diag(U)
    output_phases = [np.angle(i) for i in phases]
    return BS_list, output_phases
