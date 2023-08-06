
import sys,os

#if __name__ == "__main__":
#    basedir=os.path.abspath(os.path.dirname(__file__) + '/../..')
 #   print(basedir)
  #  os.chdir(basedir)
   # sys.path.append(basedir)

import numpy as np
import tqdm
from PyQt5.QtWidgets import QApplication, QLineEdit, QFileDialog, QDialog,QVBoxLayout,QMessageBox,QCheckBox
from PyQt5 import QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
import time
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


import pickle

from . import main_ui
from . import linklocs_ui
from .progressbar import ProgressBar

import threading
import json

import photonpy.smlm.process_movie as process_movie
import photonpy.smlm.extract_rois as extract_rois

from photonpy.smlm.util import imshow_hstack
from .qtplot import PlotDialog


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


#import photonpy.simflux.locs_to_pattern as simflux_pattern

from .drift_correct_dlg import DriftCorrectionDialog

def showMessage(txt):
   msg = QMessageBox()
   msg.setIcon(QMessageBox.Information)
   msg.setText(txt)
   msg.exec_()

class LinkLocsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = linklocs_ui.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btnBrowse.clicked.connect(self._onBrowse)
        self.ui.btnEstimate.clicked.connect(self.estimate)
    
    def setLocsFile(self,fn):
        self.ui.txtLocsFile.setText(fn)

    def _onBrowse(self):
        options = QFileDialog.Options()
#        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"", "","All Files (*);;HDF5 Files (*.hdf5)", options=options)
        if fileName:
            self.ui.txtLocsFile.setText(fileName)
            
    def estimate(self):
        from utils.link_locs import estimate_on_time
        maxdist = self.ui.maxDistance.value()
        frameskip = self.ui.frameskip.value()
        fig,bins,framecounts = estimate_on_time(self.ui.txtLocsFile.text(),maxdist,frameskip)

        import photonpy.smlm.ui.qtplot as qtplot 
        plotdlg=qtplot.PlotDialog(fig,self)
        plotdlg.setModal(True)
        plotdlg.show()

def getWidgetValues(widgets):
    d={}
    for w in widgets:
        if type(w) == QtWidgets.QDoubleSpinBox or type(w) == QtWidgets.QSpinBox:
            v = w.value()
        elif type(w) == QLineEdit:
            v = w.text()
        elif type(w) == QCheckBox:
            v = w.isChecked()
        else:
            continue
        d[w.objectName()] = v
    return d

def setWidgetValues(widgets,values):
    for w in widgets:
        if w.objectName() in values:
            v = values[w.objectName()]
            if type(w) == QtWidgets.QDoubleSpinBox or type(w) == QtWidgets.QSpinBox:
                w.setValue(v)
            elif type(w) == QLineEdit:
                w.setText(v)
            elif type(w) == QCheckBox:
                w.setChecked(v)
                
                
class Dataset:
    def __init__(self, queueResults, imgshape, cfg,label):
        self.results = queueResults
        self.label=label
        self.imgshape=imgshape
        self.cfg=cfg
        
    def info(self):
        m_crlb_x = np.median(self.results.CRLB()[:,0])
        m_bg= np.median(self.results.estim[:,3])
        m_I=np.median(self.results.estim[:,2])
        return f"#Spots: {len(self.results.estim)}. Imgsize:{self.imgshape[0]}x{self.imgshape[1]} pixels. Median CRLB X: {m_crlb_x:.2f} [pixels], bg:{m_bg:.1f}. I:{m_I:.1f}"
        
        #f"{name} - threshold={self.cfg['threshold']}, median crlb x={m_crlb_x} px, #spots={len(self.results.estim)}"

        

class Window(QDialog):
    localizeDone = QtCore.pyqtSignal()
    roiExtractionDone = QtCore.pyqtSignal()
    
    datasets = []

    def __init__(self):
        super().__init__()
        self.title = 'SIMFLUX Viewer'

        self.ui = main_ui.Ui_Dialog()
        ui=self.ui
        ui.setupUi(self)
    
        ui.btnBrowseTiff.clicked.connect(self.onBrowseTiff)
        ui.btnLocalize.clicked.connect(self.localize)
        ui.btnLinkLocs.clicked.connect(self.linklocs)
        
        ui.btnBrowseCameraDarkFrames.clicked.connect(self.onBrowseCameraDarkFrames)
        ui.btnBrowseCameraLightFrames.clicked.connect(self.onBrowseCameraLightFrames)
        ui.btnBrowseROIs.clicked.connect(self.onBrowseROIFile)
        
        ui.btnExtractROIs.clicked.connect(self.onExtractROIs)
                
        ui.checkBoxPerPixelCamCalib.toggled.connect(self.onPerPixelCamCalibChanged)
        self.onPerPixelCamCalibChanged()
        
        self.localizeDone.connect(self.onLocalizeDone)
        self.roiExtractionDone.connect(self.onROIExtractionDone)
        
        self.cfgFile = os.path.dirname(__file__) + '/ui-cfg.json'
        self.cfgWidgets = {
                ui.roisize,
                ui.gain,
                ui.offset,
                ui.detectionThreshold,
                ui.pixelsize,
                ui.psfSigmaX, ui.psfSigmaY,
                ui.tiffPath,
                ui.smlmLocsFile,
                ui.txtCameraDarkFrames,
                ui.txtCameraLightFrames,
                ui.startFrame,
                ui.maxLinkDistance,
                ui.maxLinkFrameskip,
                ui.txtROIFile,
                ui.roiExtractMinSpotFrames,
                ui.roiExtractSpotFrames,
                ui.roiExtractAppend,
                ui.maxLinkDistanceIntensity,
                ui.checkBoxPerPixelCamCalib
                }
        self.load()
        
    def onPerPixelCamCalibChanged(self):
        v = self.ui.checkBoxPerPixelCamCalib.checkState()
        self.ui.offset.setEnabled(not v)
        self.ui.gain.setEnabled(not v)
        self.ui.txtCameraDarkFrames.setEnabled(v)
        self.ui.txtCameraLightFrames.setEnabled(v)

        
    def onDriftCorrection(self):
        dlg = DriftCorrectionDialog(self, self.ui.smlmLocsFile.text())
        dlg.show()
        
    def load(self):
        path = os.path.abspath(os.curdir+"/"+self.cfgFile)
        print(f"Loading UI state from {path}")
        if os.path.exists(self.cfgFile):
            with open(self.cfgFile,'r') as f:
                d = json.load(f)
                setWidgetValues(self.cfgWidgets,d)
        
    def save(self):
        d = getWidgetValues(self.cfgWidgets)
        with open(self.cfgFile,'w') as f:
            json.dump(d,f,indent=4)
        
    def closeEvent(self,event):
        self.save()
        
    def linklocs(self):
        dlg = LinkLocsDialog(self)
        dlg.setLocsFile(self.ui.smlmLocsFile.text())
        dlg.show()
        
    def updatePaths(self):
        tiff_path = self.ui.tiffPath.text()
        locs_fn = os.path.splitext(tiff_path)[0]+".hdf5"
        self.ui.smlmLocsFile.setText(locs_fn)
                
        rois_path = os.path.splitext(tiff_path)[0]+".rois"
        self.ui.txtROIFile.setText(rois_path)        
        
        
    def onBrowseCameraDarkFrames(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse movie containing dark calibration:", "","All Files (*);;TIFF File (*.tif)", options=options)
        if fileName:
            self.ui.txtCameraDarkFrames.setText(fileName)

    def onBrowseCameraLightFrames(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse movie containing light frames for calibration:", "","All Files (*);;TIFF File (*.tif)", options=options)
        if fileName:
            self.ui.txtCameraLightFrames.setText(fileName)

    def onBrowseROIFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse ROI file", "","All Files (*);;TIFF File (*.tif)", options=options)
        if fileName:
            self.ui.txtROIFile.setText(fileName)

    def onBrowseTiff(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Browse TIFF", "","All Files (*);;TIFF File (*.tif)", options=options)
        if fileName:
            self.ui.tiffPath.setText(fileName)
            self.updatePaths()

        
    def onExtractROIs(self):
        locs_fn = self.ui.smlmLocsFile.text()
        tiff_path = self.ui.tiffPath.text()
        rois_path = self.ui.txtROIFile.text()

        pbar = ProgressBar("Extracting ROIs and estimating spot background and intensity")
        def progress_update(msg,done):
            if msg is not None:
                pbar.setMsg.emit(msg)
            if done is not None:
                pbar.update.emit(done)
            return not pbar.abortPressed
        
        cfg = self.getConfig()

        cfg = {**cfg,
             'maxlinkdistXY': self.ui.maxLinkDistance.value(),
             'maxlinkdistI': self.ui.maxLinkDistanceIntensity.value(),
             'maxlinkframeskip': self.ui.maxLinkFrameskip.value()
             }
        
        maxroiframes = self.ui.roiExtractSpotFrames.value()
        minroiframes = self.ui.roiExtractMinSpotFrames.value()
        appendFrames = self.ui.roiExtractAppend.value()
        
        def process_thread():
            self.rois,self.roiframes = extract_rois.extract_rois(rois_path, tiff_path, cfg, minroiframes, 
                                      maxroiframes, appendFrames, locs_fn, progress_update)
            if not pbar.abortPressed:             
                self.roiExtractionDone.emit()
            
        t = threading.Thread(target=process_thread)
        t.start()
        pbar.show()
        
    def onViewROIs(self):
        rois_path = self.ui.txtROIFile.text()
        roidata = extract_rois.ROIData.load(rois_path)
        
        plt.figure()
        for k in range(20):
            imshow_hstack(roidata.frames[k])

    def updateList(self):
        model = QtGui.QStandardItemModel()
        self.ui.listDatasets.setModel(model)
        
        for d in self.datasets:
            item = QtGui.QStandardItem(f"{d.label} - {d.info()}")   
            model.appendRow(item)


    def getConfig(self):
        offset = self.ui.offset.value()
        gain = self.ui.gain.value()

        if self.ui.checkBoxPerPixelCamCalib.isChecked():
            offset = self.ui.txtCameraDarkFrames.text()
            gain = self.ui.txtCameraLightFrames.text()
            
            if len(offset) == 0:
                showMessage('Need to provide movie with dark frames')
                return
            
            if len(gain) == 0:
                showMessage('Need to provide movie with light frames')
                return 
        
        sigmaX = self.ui.psfSigmaX.value()
        sigmaY = self.ui.psfSigmaY.value()
        
        cfg = {
                'sigma': [sigmaX, sigmaY],
                'roisize': self.ui.roisize.value(),
                'threshold': self.ui.detectionThreshold.value(),
                'gain': gain,
                'offset': offset,
                'startframe': self.ui.startFrame.value(),
                'maxchisq': self.ui.chiSquareThreshold.value()
            }
        return cfg
        
    def localize(self):
        tiff_path = self.ui.tiffPath.text()
        if not os.path.exists(tiff_path):
            return
        
        cfg = self.getConfig()
        if cfg is None:
            return
        
        locs_fn = self.ui.smlmLocsFile.text()
        est_sigma = self.ui.checkEstimSigma.isChecked()
        
        self.ui.labelLocsInfo.setText('')
        
        pbar = ProgressBar("Running spot detection and 2D Gaussian localization...")

        def progress_update(msg,done):
            if msg is not None:
                pbar.setMsg.emit(msg)
            if done is not None:
                pbar.update.emit(done)
            return not pbar.abortPressed
        
        def localize_thread():
            print (f"Localize thread: {threading.get_ident()}")
            self.results, self.imgshape = process_movie.localize(tiff_path, cfg, locs_fn, progress_update, est_sigma)
            self.cfg = cfg
            self.tiff_path = tiff_path
            if not pbar.abortPressed:
                self.localizeDone.emit()
            
        t = threading.Thread(target=localize_thread)
        t.start()
        
        pbar.show()

    @QtCore.pyqtSlot()
    def onLocalizeDone(self):
        print("localize done")
                
        if 'sx' in self.results.colnames:
            sx = self.results.estim[:, self.results.ColIdx('sx')]
            sy = self.results.estim[:, self.results.ColIdx('sy')]
            self.ui.psfSigmaX.setValue(np.median(sx))
            self.ui.psfSigmaY.setValue(np.median(sy))
            
            fig = plt.figure(figsize=(8,5))
            plt.hist([sx,sy],label=['Sigma X','Sigma Y'],range=(1,3),bins=100)
            plt.legend()
            plt.xlabel('PSF Sigma [pixels]')
            plt.show()
            #PlotDialog(fig).show()
                
        name = os.path.split(self.tiff_path)[1]
        self.datasets = [ Dataset(self.results, self.imgshape, self.cfg, name) ]
        self.updateList()

        #self.ui.labelLocsInfo.setText(self.datasets[0].info())
        

    @QtCore.pyqtSlot()
    def onROIExtractionDone(self):
        print("roi extraction done")
        
def run_ui():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
       
    wnd = Window()
    wnd.show()
    wnd.activateWindow()
    app.exec_()
#    del tqdm    # prevent exception at exit about not being able to join thread
    del app     # prevent IPython+Qt issue https://github.com/spyder-ide/spyder/issues/2970

if __name__ == '__main__':
    run_ui()