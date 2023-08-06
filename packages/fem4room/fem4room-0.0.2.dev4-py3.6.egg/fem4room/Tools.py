import sys
import numpy as np
import scipy.sparse as sparse
import scipy.signal as signal
import scipy.fft as fft
import pickle as pk
import gmsh
import numpy.linalg as la
from . import TimeEngine,Boundary
from . import FEM_3D as fem3d
from . import FEM_2D as fem2d

class Sources():

    @staticmethod
    def monopole_by_band(t_,band,sigma=None):
        """ Return a forcing function representing a monopole source with max amplitude 1 at 1 meter. 
        The signal is a gaussian with the given cutoff frequencies (3dB). """
        freq = (np.max(band)+np.min(band))/2 #Center frequency
        omega = 2*np.pi*freq

        if sigma==None:
            fc = (np.max(band)-np.min(band))
            sigma=1/(2*np.pi*fc/4) #TODO: What is the best sigma? To be studied

        t=t_-5*sigma #Shifts the gaussian so it can start at zero.

        _signal = np.sin(omega*t) * np.exp(-t**2/(2*sigma**2))
        _signal = _signal/np.max(np.abs(_signal))
        return 4 * np.pi * _signal

class Visualization():
    @staticmethod
    def addView(mesh,viewName,timeData,nodeTags):
        """timeData must be (Timesteps)x(#dof)"""
        viewTag = mesh.pos.add(viewName)
        for i_timeData in range(0,len(timeData)):
            mesh.pos.addModelData(viewTag,i_timeData,mesh.name,'NodeData',nodeTags,timeData[i_timeData].reshape(-1,1),numComponents=1)

    @staticmethod
    def showTime(mesh,viewNames,data,view_dofs,fltkrun=True):
        """data must be (Views)x(Timesteps)x(#dof)"""
        for i_view in range(0,len(data)):
            nodeTags = mesh.nodeTags[view_dofs[i_view]]
            timeData = data[i_view]
            Visualization.addView(mesh,viewNames[i_view],timeData,nodeTags)

        if (fltkrun):
            mesh.FLTKRun()

class SaveLoad():
    def save(self,name,saved_dofs,dof,sln,sln_main,tspan):
        """Save the mesh and the main infos about the numerical result."""
        self.dof = dof
        self.sln = sln
        self.sln_main = sln_main
        self.tspan = tspan
        self.saved_dofs = saved_dofs
        gmsh.option.setNumber('Mesh.SaveAll',1)
        gmsh.write('data/' + name + '.msh')
        with open('data/' + name + '.pickle', 'wb') as f:
            pk.dump(self, f, pk.HIGHEST_PROTOCOL)

    def load(self,name,m):
        """Load the mesh and the main infos about a numerical result."""
        gmsh.open('data/' + name + '.msh')
        m.readMsh('data/' + name + '.msh')
        with open('data/' + name + '.pickle', 'rb') as f:
            T = pk.load(f)
            self.dof = T.dof
            self.sln = T.sln
            self.sln_main = T.sln_main
            self.tspan = T.tspan
            self.saved_dofs = T.saved_dofs

class Other():
    @staticmethod
    def nearest_dof(dofs,x):
        """Return the index of the nearest 3D degree of freedom"""
        idx = np.argmin(la.norm(dofs - x,axis=1))
        return idx

    @staticmethod
    def printInline(text):
        sys.stdout.write(text + '                                            \r')

    @staticmethod
    def wiener_deconvolution(output, input, SNR=1):
        input = np.hstack((input, np.zeros(len(output) - len(input)))) # zero pad the kernel to same length
        H = fft.fft(input)
        deconvolved = np.real(fft.ifft(fft.fft(output)*np.conj(H)/(H*np.conj(H) + SNR**2)))
        return deconvolved