"""
Example of using the photonpy library to process 2D fret/cosmos image data. 
Use pip install photonpy=1.0.24
"""
import numpy as np
import matplotlib.pyplot as plt
from photonpy import Context, Gaussian
from photonpy.smlm.process_movie import localize
from photonpy.smlm.extract_rois import extract_rois
import os

if not os.path.exists('movie.tif'):
    from . import generate_example_data
    generate_example_data.generate()

roisize = 10

cfg = { 
        'sigma': 2, # psf width for detection and initial estimate
        'roisize': roisize,
        'gain': 1,  # change this for real cameras
        'offset': 0,
        'threshold': 5, # spot detection threshold. This needs some manual tweaking
       
        'maxlinkdistXY': 1,  # [pixels], typically set to 2*CRLB
        'maxlinkdistI': 1000,
        'maxlinkframeskip': 2  # how many frames can the spot be undetected/off while still being the same molecule
}

locs_fn = 'movie_locs.hdf5'

r,_ = localize('movie.tif', cfg, output_file=locs_fn, estimate_sigma=True)
psf_sigma = np.median(r.estim[:,4])

rois,frames = extract_rois('movie.tif', locs_fn = locs_fn, 
                           cfg= cfg, 
                           minroiframes=10,  # minimum trace length
                           maxroiframes=200)  #max trace length

trace_length = rois['numframes']
trace_rois = [frames[i,:trace_length[i]] for i in range(len(frames))]
trace_cornerpos = rois['cornerpos']
trace_startpos = rois['startframe']

with Context() as ctx:
    psf = Gaussian(ctx).CreatePSF_XYIBg(roisize, psf_sigma, cuda=True)
    trace_intensities = [psf.Estimate(tr_rois)[0][:,2] for tr_rois in trace_rois]

# plot the first 10 traces
plt.figure()
for i in range(10):
    plt.plot(trace_intensities[i])
plt.title('A subset of intensities')
    
plt.figure()
plt.hist(trace_length)
plt.title('trace lengths')

