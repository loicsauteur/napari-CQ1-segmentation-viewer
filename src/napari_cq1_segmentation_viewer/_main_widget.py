"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
import os
from typing import TYPE_CHECKING

from magicgui import magic_factory
from magicgui.widgets import FileEdit
from qtpy.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QCheckBox

from skimage import io

if TYPE_CHECKING:
    import napari


class CQ1Viewer(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        self.raw_label = QLabel('Raw image folder:')
        self.raw_dir = FileEdit(mode='d')
        self.raw_dir.changed.connect(self._check_raw_path)
        self.raw_indiator = QLabel('Not valid')
        self.raw_indiator.setStyleSheet('color: red')
        self.raw_valid = False

        self.seg_label = QLabel('Segmentation image folder:')
        self.seg_dir = FileEdit(mode='d')
        self.seg_dir.changed.connect(self._check_seg_path)
        self.seg_indicator = QLabel("Not valid")
        self.seg_indicator.setStyleSheet('color: red')
        self.seg_valid = False

        # list of files that are available
        self.wells = []
        self.fovs = []
        self.chooseWell = QLabel('Choose a well:')
        self.wells_list = QComboBox()
        self.wells_list.currentTextChanged.connect(self._well_changed)
        self.wells_list.setDisabled(True)
        self.chooseFOV = QLabel('Choose a FOV')
        self.fov_list = QComboBox()
        self.fov_list.setDisabled(True)

        # button to load images
        self.loadButton = QPushButton('Load images')
        self.loadButton.setDisabled(True)
        self.loadButton.clicked.connect(self._load_images)
        self.clearViewer = QCheckBox('Close already open images')
        self.clearViewer.setChecked(True)

        # consturct the layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.raw_label)
        self.layout().addWidget(self.raw_dir.native)
        self.layout().addWidget(self.raw_indiator)
        self.layout().addWidget(self.seg_label)
        self.layout().addWidget(self.seg_dir.native)
        self.layout().addWidget(self.seg_indicator)
        self.layout().addWidget(self.chooseWell)
        self.layout().addWidget(self.wells_list)
        self.layout().addWidget(self.chooseFOV)
        self.layout().addWidget(self.fov_list)
        self.layout().addWidget(self.loadButton)
        self.layout().addWidget(self.clearViewer)


    def _load_images(self):
        # close possibly open images
        if self.clearViewer.isChecked():
            self.viewer.layers.clear()
        # load images
        wellID = self.wells_list.currentText()
        fovID = self.fov_list.currentText()
        imageID = wellID + fovID

        # load raw images
        rawPaths = {}
        channels = []
        for file in os.listdir(str(self.raw_dir.value) + '/'):
            if file.startswith(imageID):
                if not (file[-6:] in channels):
                    channels.append(file[-6:])
        ## create path directioy
        for c in channels:
            rawPaths[c.replace('.tif', '')] = str(self.raw_dir.value) + '/' + imageID + "*" + c
        # add the images to the viewer
        for k, v in rawPaths.items():
            imCol = io.imread_collection(v)
            imStack = io.concatenate_images(imCol)
            self.viewer.add_image(imStack, name=k, blending='additive')

        # load segmentations
        segPaths = {}
        for file in os.listdir(str(self.seg_dir.value) + '/'):
            if file.startswith(imageID):
                segPaths[file] = str(self.seg_dir.value) + '/' + file
        for k, v in segPaths.items():
            img = io.imread(v)
            self.viewer.add_labels(img, name=k.replace(imageID + '_', ''), blending='additive')




    def _well_changed(self, s):
        # update the fov dropdown
        self.change_fov_dropList(s)

    def create_fileList(self):
        # reset the dropdowns and their lists
        self.wells = []
        self.fovs = []
        self.wells_list.setDisabled(True)
        self.fov_list.setDisabled(True)
        self.wells_list.clear()
        self.fov_list.clear()
        # disable the load button
        self.loadButton.setDisabled(True)

        if self.seg_valid and self.raw_valid:
            files = [f for f in os.listdir(str(self.seg_dir.value) + '/')]
            for f in files:
                if f.startswith('W') and f.endswith('.tif'):
                    wellID = f[0:5]
                    if not (wellID in self.wells):
                        self.wells.append(wellID)

        if len(self.wells) > 0:
            self.wells_list.setDisabled(False)
            self.wells_list.addItems(self.wells)
            self.fov_list.setDisabled(False)
            # populte also the FOVs dropdown
            self.change_fov_dropList(self.wells_list.currentText())
            # enable the load button
            self.loadButton.setDisabled(False)


    def change_fov_dropList(self, wellID):
        # reset the dropdown list
        self.fovs = []
        self.fov_list.clear()

        files = [f for f in os.listdir(str(self.seg_dir.value) + '/')]
        for f in files:
            if f.startswith(wellID) and f.endswith('.tif'):
                fovID = f[5:10]
                if not (fovID in self.fovs):
                    self.fovs.append(fovID)
        # add the fovs to the dropdown
        self.fov_list.addItems(self.fovs)




    def _check_raw_path(self):
        files = [f for f in os.listdir(str(self.raw_dir.value) + '/')]
        for f in files:
            if f.startswith('W') and f.endswith('C1.tif'):
                self.raw_valid = True
                self.raw_indiator.setText('Valid')
                self.raw_indiator.setStyleSheet('color: green')
                self.create_fileList()
                return
        self.raw_valid = False
        self.raw_indiator.setText('Not Valid')
        self.raw_indiator.setStyleSheet('color: red')
        self.create_fileList()


    def _check_seg_path(self):
        files = [f for f in os.listdir(str(self.seg_dir.value) + '/')]
        for f in files:
            if f.startswith('W') and f.endswith('_nuclei.tif'):
                self.seg_valid = True
                self.seg_indicator.setText('Valid')
                self.seg_indicator.setStyleSheet('color: green')
                self.create_fileList()
                return
        self.seg_valid = False
        self.seg_indicator.setText('Not valid')
        self.seg_indicator.setStyleSheet('color: red')
        self.create_fileList()

