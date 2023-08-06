# -*- coding: utf-8 -*-

import os
from photonpy import Context, PostProcessMethods
import numpy as np
from photonpy.smlm.picasso_hdf5 import load as load_hdf5, save as save_hdf5
from photonpy.smlm.frc import FRC
from photonpy.smlm.drift_estimate import minEntropy,rcc
import tqdm

class Dataset:
    """
    Keep a localization dataset using numpy structured array
    """
    def __init__(self, length, dims, imgshape=None, estim=None, framenum=None,  crlb=None, origin=None,pixelsize=1,chisq=None):

        self.createDTypes(dims, len(imgshape))
        
        self.imgshape = imgshape 
        self.data = np.recarray(length, dtype=self.dtypeLoc)
        self.data.fill(0)
        self.origin = origin
        self.pixelsize = pixelsize
        self.sigma = np.zeros(dims)

        if estim is not None:
            if np.can_cast(estim.dtype, self.dtypeEstim):
                self.data.estim = estim
            else:
                # Assuming X,Y,[Z,]I,bg
                self.data.estim.pos = estim[:,:dims]
                self.data.estim.photons = estim[:,-2]
                self.data.estim.bg = estim[:,-1]
            
        if crlb is not None:
            if np.can_cast(crlb.dtype, self.dtypeEstim):
                self.data.crlb = crlb
            else:
                self.data.crlb.pos = crlb[:,:dims]
                self.data.crlb.photons = crlb[:,-2]
                self.data.crlb.bg = crlb[:,-1]
            
        if chisq is not None:
            self.data.chisq = chisq
        
        if framenum is not None:
            self.data.frame = framenum
        
            
    def createDTypes(self,dims, imgdims):
        """
        Can be overriden to add columns
        """
        self.dtypeEstim = np.dtype([
            ('pos', np.float32, (dims,)),
            ('photons', np.float32),
            ('bg', np.float32)])
        
        self.dtypeLoc = np.dtype([
            ('frame', np.int32),
            ('estim', self.dtypeEstim),
            ('crlb', self.dtypeEstim),
            ('chisq', np.float32),
            ('roipos', np.int32, (imgdims,))
            ])

            
    def filter(self, indices):
        count = len(self)
        self.data = self.data[indices]
        return count-len(self.data)
    
    @property
    def numFrames(self):
        return np.max(self.data.frame)+1
            
    def indicesPerFrame(self):
        frame_indices = self.data.frame
        if len(frame_indices) == 0: 
            numFrames = 0
        else:
            numFrames = np.max(frame_indices)+1
        frames = [[] for i in range(numFrames)]
        for k in range(len(self.data)):
            frames[frame_indices[k]].append(k)
        for f in range(numFrames):
            frames[f] = np.array(frames[f], dtype=int)
        return frames
            
    def __len__(self):
        return len(self.data)
    
    @property
    def dims(self):
        return self.data.estim.pos.shape[1]
    
    @property
    def pos(self):
        return self.data.estim.pos
    
    @property
    def crlb(self):
        return self.data.crlb
    
    @property
    def photons(self):
        return self.data.estim.photons
    
    @property
    def framenum(self):
        return self.data.frame
    
    def __repr__(self):
        return f'Dataset with {len(self)} {self.dims}D localizations.'

    def FRC2D(self, zoom=10, display=True,pixelsize=None):
        return FRC(self.pos, self.photons, zoom, self.imgshape, pixelsize, display=display)

    def undriftMinEntropy(self, framesPerBin=10, **kwargs):
        sigma = np.mean(self.data.crlb.pos, 0)
        
        drift, _, est_precision = minEntropy(self.data.estim.pos, 
                   self.data.frame, 
                   self.data.crlb.pos, framesperbin=framesPerBin,
                   imgshape=self.imgshape, sigmaPrecise=sigma,pixelsize=self.pixelsize, **kwargs)

        self.applyDrift(drift)
        return drift, est_precision
        
    def applyDrift(self, drift):
        self.data.estim.pos -= drift[self.data.frame]
        
    def align(self, other):
        
        def make_xyI(ds):
            r=np.zeros((len(ds),3))
            r[:,:2] = ds.pos[:,:2]
            r[:,2] = ds.photons
            return r
        
        xyI = np.concatenate([make_xyI(self), make_xyI(other)])
        framenum = np.concatenate([np.zeros(len(self),dtype=np.int32), np.ones(len(other),dtype=np.int32)])
        
        return rcc(xyI, framenum, 2, np.max(self.imgshape), maxdrift=10,RCC=False)[0][1]

    @property
    def fields(self):
        return self.data.dtype.fields
    

    @staticmethod
    def load(fn):
        ext = os.path.splitext(fn)[1]
        if ext == '.hdf5':
            estim, framenum, crlb, imgshape, sx,sy = load_hdf5(fn)
            
            numcoords = estim.shape[1]-2
            
            return Dataset(len(estim), numcoords, 
                           imgshape, estim, framenum=framenum, crlb=crlb)
        else:
            raise ValueError('unknown extension')

    def cluster(self, maxDistance, debugMode=False):
        with Context(debugMode=debugMode) as ctx:
                        
            def callback(startidx, counts, indices):
                print(f"Callback: {startidx}. counts:{len(counts)} indices:{len(indices)}")
                                                        
            clusterPos, clusterCrlb, mapping = PostProcessMethods(ctx).ClusterLocs(
                self.pos, self.crlb.pos, maxDistance)
                    
        print(f"Computing cluster properties")
        
        counts = np.bincount(mapping)
        def getClusterData(org):
            r = np.recarray( len(counts), dtype=self.dtypeEstim)
            r.photons = np.bincount(mapping, org.photons) / counts
            r.bg = np.bincount(mapping, org.bg) / counts
            for k in range(self.dims):
                r.pos[:,k] = np.bincount(mapping, org.pos[:,k]) / counts
            return r
                
        clusterEstim = getClusterData(self.data.estim)
        clusterCrlb = getClusterData(self.data.crlb)
        
        ds = Dataset(len(clusterPos), self.dims, self.imgshape, clusterEstim, np.zeros(len(clusterEstim)), crlb=clusterCrlb)
        ds.sigma = np.ones(self.dims)*maxDistance
        
        clusters = [[] for i in range(len(ds))]
        for i in range(len(mapping)):
            clusters[mapping[i]].append(i)
        for i in range(len(clusters)):
            clusters[i] = np.array(clusters[i])
        
        return ds, mapping, clusters#clusterPos, clusterCrlb, mapping 
    
    def save(self,fn):
        ext = os.path.splitext(fn)[1]
        if ext == '.hdf5':
            
            estim = np.ascontiguousarray(self.data.estim).view(np.float32).reshape((len(self),2+self.dims))
            crlb = np.ascontiguousarray(self.data.crlb).view(np.float32).reshape((len(self),2+self.dims))
            
            save_hdf5(fn, estim, crlb, self.framenum, self.imgshape, self.sigma[0], self.sigma[1])
        else:
            raise ValueError('unknown extension')
    
    @staticmethod
    def fromQueueResults(qr, imgshape):
        ds = Dataset(len(qr.estim), qr.estim.shape[1]-2, imgshape=imgshape, estim=qr.estim,
                     framenum=qr.ids, crlb=qr.crlb, chisq=qr.chisq)
        return ds
    
    