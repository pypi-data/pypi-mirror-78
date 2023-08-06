

import ctypes
import scipy.io
import numpy as np
import numpy.ctypeslib as ctl

from . import estimator
from .context import Context


class BSplinePSF_Params(ctypes.Structure):
    _fields_ = [
        ("dimension", ctypes.c_int),
        ("degree", ctypes.c_int),
        ("n_pixels", ctypes.c_int),
        ("n_tri", ctypes.c_int),
        ("tri", ctl.ndpointer(ctypes.c_int, flags="C_CONTIGUOUS")),
        ("n_phi", ctypes.c_int),
        ("phi", ctl.ndpointer(np.float32, flags="C_CONTIGUOUS")),
        ("coefs", ctl.ndpointer(np.float32, flags="C_CONTIGUOUS")),
        ("coefs_x", ctl.ndpointer(np.float32, flags="C_CONTIGUOUS")),
        ("coefs_y", ctl.ndpointer(np.float32, flags="C_CONTIGUOUS")),
        ("coefs_z", ctl.ndpointer(np.float32, flags="C_CONTIGUOUS")),
    ]

    def __init__(self, dimension, degree, n_pixels, n_zslices, n_stacks, z_range, tri, phi, coefs, coefs_x, coefs_y, coefs_z):
        self.dimension = dimension
        self.degree = degree
        self.n_pixels = n_pixels

        # parameters that are available only from python code
        self.n_zslices = n_zslices
        self.n_stacks = n_stacks
        self.z_range = z_range
        self.zrange = [-z_range/2.0, z_range/2.0]
        ###

        self.n_tri = tri.shape[0]
        self.n_phi = phi.shape[0]

        self.coefs_data = np.ascontiguousarray(coefs, dtype=np.float32)
        self.coefs = self.coefs_data.ctypes.data
        self.coefs_x_data = np.ascontiguousarray(coefs_x, dtype=np.float32)
        self.coefs_x = self.coefs_x_data.ctypes.data
        self.coefs_y_data = np.ascontiguousarray(coefs_y, dtype=np.float32)
        self.coefs_y = self.coefs_y_data.ctypes.data
        self.coefs_z_data = np.ascontiguousarray(coefs_z, dtype=np.float32)
        self.coefs_z = self.coefs_z_data.ctypes.data

        self.tri_data = np.ascontiguousarray(tri, dtype=np.int32)
        self.tri = self.tri_data.ctypes.data
        self.phi_data = np.ascontiguousarray(phi, dtype=np.float32)
        self.phi = self.phi_data.ctypes.data

    def __str__( self ):
        """Print the parameters"""

        s = f'dimension = {self.dimension}\n'
        s += f'degree = {self.degree}\n'
        s += f'ROI = {self.n_pixels}\n'
        s += f'n_tri = {self.n_tri}\n'
        s += f'n_phi = {self.n_phi}\n'
        s += f'n_zslices = {self.n_zslices}\n'
        s += f'n_stacks = {self.n_stacks}\n'
        s += f'z_range = {self.z_range}\n'

        return s

    @classmethod
    def from_file(cls, spline_filename):
        mat = scipy.io.loadmat(spline_filename)
        spline = mat["spline"]
        spline_x = mat["spline_x"]
        spline_y = mat["spline_y"]
        spline_z = mat["spline_z"]

        degree = spline["degree"]
        dimension = spline["dim"]
        n_pixels = mat["n_pixels"]

        try:
            n_zslices = mat["n_zslices"][0][0]
            n_stacks = mat["n_stacks"][0][0]
            z_range = mat["z_range"][0][0]
        except:
            print( 'WANRNING: n_zsplices, n_stacks and z_range '
                   'have not been set' )
            n_zslices = None
            n_stacks = None
            z_range = None

        tri = spline["TRI"][0][0]
        phi = spline["PHI"][0][0]
        coefs = spline["coefs"][0][0]
        coefs_x = spline_x["coefs"][0][0]
        coefs_y = spline_y["coefs"][0][0]
        coefs_z = spline_z["coefs"][0][0]

        return cls(dimension, degree, n_pixels, n_zslices, n_stacks, z_range, tri, phi, coefs, coefs_x, coefs_y, coefs_z)


class BSpline:
    def __init__(self, ctx: Context):
        smlmlib = ctx.lib
        self.ctx = ctx

        self._BSpline_CreatePSF_XYZIBg = smlmlib.BSpline_CreatePSF_XYZIBg
        self._BSpline_CreatePSF_XYZIBg.restype = ctypes.c_void_p
        self._BSpline_CreatePSF_XYZIBg.argtypes = [
            ctypes.c_int,  # roisize
            ctypes.POINTER(BSplinePSF_Params),
            ctypes.c_int,  # cuda
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

    def CreatePSF_XYZIBg(self, roisize, calib: BSplinePSF_Params, cuda, scmos=None) -> estimator.Estimator:
        inst = self._BSpline_CreatePSF_XYZIBg(roisize, calib, cuda, scmos.inst if scmos else None, self.ctx.inst)
        return estimator.Estimator(self.ctx, inst, calib)
    
    