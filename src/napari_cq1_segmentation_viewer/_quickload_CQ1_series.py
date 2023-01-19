import os
from typing import TYPE_CHECKING

from napari_cq1_segmentation_viewer.cq1_utils.utils_cq1 import getWellName

if TYPE_CHECKING:
    import napari

from qtpy.QtWidgets import QVBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtCore import pyqtSignal

from skimage import io


class Quickload_CQ1_series(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        # Create a QLabel that accepts drops
        self.dropZone = DropLabel('Drop a CQ1 TIF image here\n(No timelapse support)')
        self.dropZone.myChange.connect(self._dropEvent)

        # construct the layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.dropZone)



    def _dropEvent(self):
        filepath = self.dropZone.filepath
        filename = self.dropZone.filename

        dir = filepath.replace(filename, '')
        # check if the dir path exists, Unix systems need a leading /
        if not os.path.exists(dir):
            dir = '/' + dir
            if not os.path.exists(dir):
                print('Something went wrong. No folder:\n\t', dir)
                return
        # check if file is a CQ1 image and open it
        if filename.startswith('W') and filename.endswith('.tif'):
            self.openTifImage(dir, filename)
        else:
            print('File not valid!')

    def openTifImage(self, path, name):
        # get a list of files matching the well ID (and FOV)
        wellID = name[0:10] # WellID+FOVID
        convID = getWellName(wellID[0:5])
        dirList = [f for f in os.listdir(path) if f.startswith(wellID)]
        dirList.sort()
        # get a list of available channels
        channels = []
        for f in dirList:
            if f[-6:-4] not in channels:
                channels.append(f[-6:-4])

        # open tifs if they are not stacks
        if len(channels) == len(dirList):
            for i in dirList:
                img = io.imread(path + i)
                self.viewer.add_image(img, name=i + ' (' + convID + ')', blending='additive')
        else:
            # open stacks
            pathDic = {}
            for c in channels:
                pathDic[wellID + '_' + c] = path + wellID + '*' + c + '.tif'
            for name, path in pathDic.items():
                imCol = io.imread_collection(path)
                imStack = io.concatenate_images(imCol)
                self.viewer.add_image(imStack, name=name + ' (' + convID + ')', blending='additive')


class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 100)
        self.filepath = ''
        self.filename = ''
        self.setToolTip('Drag and drop a CQ1 TIF image here!')
        self.setStyleSheet('background: grey')


    # add a signal to the class
    myChange = pyqtSignal()



    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()


    def dropEvent(self, event):
        url = event.mimeData().urls()[0] # this actually takes urls of all dropped files

        filename = str(url.fileName())
        filepath = str(url.path())
        event.acceptProposedAction()

        if (filename.endswith('.tif')):
            # strip the leading / from the url (one too much for Windows systems, unlike Unix)
            self.filepath = filepath.strip('/')
            self.filename = filename
            self.myChange.emit()
        else:
            print('Not a TIF file.')