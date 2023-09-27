"""
Created on 27.09.2023
@author: olivier pelhatre
"""
import sys
import os
from PySide6 import QtWidgets, QtCore
from Radar_Olivier_GUI import Ui_MainWindow
from read_frtm_1 import read_frtm
from utils import get_results_files
from scipy import signal
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import matplotlib.pyplot as plt
import qdarkstyle
import OpenGL

os.system('cls')

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DesignerMainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
        self.n = 0
        self.ovsp1 = 16
        self.ovsp2 = 16
        # self.ovsp3 = 1
        self.timer = QtCore.QTimer()

        # Signals/Slots
        self.actionLoad_Directory.triggered.connect(self.loadDir)
        self.actionStop_timer.triggered.connect(self.stopTimer)
        self.actionRe_Start_Timer.triggered.connect(self.startTimer)
        self.spinBox.valueChanged.connect(self.setInterval)

        # Plots definition
        # 1. Power vs Range
        p1 = pg.PlotWidget()
        p1.setTitle('Power (dBm) vs Range (m)', color='w', size='10pt')
        self.gridLayout.addWidget(p1, 0, 0, 1, 1)
        self.p1_item = p1.plot(pen='r')
        p1.setLabel(axis='left', text='Power (dBm)')
        p1.setLabel(axis='bottom', text='Range (m)')
        p1.getAxis('left').setTextPen('w')
        p1.getAxis('bottom').setTextPen('w')
        p1.showGrid(x=True, y=True, alpha=1)

        # 2. Power vs Range (Top View)
        p2 = pg.PlotWidget()
        p2.setTitle('Range (m) vs Channel', color='w', size='10pt')
        self.gridLayout.addWidget(p2, 0, 1, 1, 1)
        self.img2 = pg.ImageItem(border='w')
        p2.addItem(self.img2)
        self.img2.setColorMap(pg.colormap.get('CET-D1A'))
        # rect2 = QtCore.QRectF(0, 0, 8, 3)
        p2.setLabel(axis='left', text='Range (m)')
        p2.setLabel(axis='bottom', text='Channel')
        p2.getAxis('left').setTextPen('w')
        p2.getAxis('bottom').setTextPen('w')

        # 3. Angle of Arrival vs Range (Surface)
        w = gl.GLViewWidget()
        self.gridLayout.addWidget(w, 1, 0, 1, 1)
        # g = gl.GLGridItem()
        # g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
        # w.addItem(g)
        # xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
        # xLabel.setGLViewWidget(w)
        # w.addItem(xLabel)
        self.p3 = gl.GLSurfacePlotItem(computeNormals=False, smooth=True)
        w.addItem(self.p3)

        # 4. Angle of Arrival vs Range
        p4 = pg.PlotWidget()
        p4.setTitle('Range (m) vs Angle (deg)', color='w', size='10pt')
        self.gridLayout.addWidget(p4, 1, 1, 1, 1)
        self.img4 = pg.ImageItem(border='w')
        p4.addItem(self.img4)
        self.img4.setColorMap(pg.colormap.get('CET-D1A'))
        p4.setLabel(axis='left', text='Range (m)')
        p4.setLabel(axis='bottom', text='Angle (deg)')
        p4.getAxis('left').setTextPen('w')
        p4.getAxis('bottom').setTextPen('w')

        # 5. Doppler Velocity vs Range
        p5 = pg.PlotWidget()
        p5.setTitle('Doppler Velocity vs Range (m)', color='w', size='10pt')
        self.gridLayout.addWidget(p5, 2, 0, 1, 2)
        self.img5 = pg.ImageItem(border='w')
        p5.addItem(self.img5)
        self.img5.setColorMap(pg.colormap.get('CET-D1A'))
        p5.setLabel(axis='left', text='Range (m)')
        p5.setLabel(axis='bottom', text='Doppler Velocity (m/s)')
        p5.getAxis('left').setTextPen('w')
        p5.getAxis('bottom').setTextPen('w')

    def closeEvent(self, event):  # Use if the main window is closed by the user
        close = QtWidgets.QMessageBox.question(self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.stopTimer()
            self.close()
            event.accept()
            app.quit()
        else:
            event.ignore()

    def stopTimer(self):
        self.timer.stop()

    # def startTimer(self):
    #     self.timer.timeout.connect(self.updatePlot)
    #     self.timer.start(self.spinBox.value())
    #     self.timer.setInterval(self.spinBox.value())

    def loadDir(self):
        self.timer.stop()
        self.n = 0

        self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select '.results' Directory")
        self.results_files = get_results_files(self.dir_path)

        # Read datas from first frtm file in order to calculate important RADAR parameters
        self.data = read_frtm(self.results_files[0])  # number of variation in the parametric setup
        self.nchirp = self.data.ntime
        self.nfreq = self.data.nfreq
        self.nchannels = self.data.num_channels
        self.range_resolution = self.data.range_resolution()
        self.range_period = self.data.range_period()
        self.velocity_period = self.data.velocity_period()
        self.velocity_resolution = self.data.velocity_resolution()

        # Define the result array
        self.raw_data = np.empty((self.nfreq, self.nchirp, self.nchannels), dtype=complex)

        # Calculate x, y axes min and max
        self.rect2 = QtCore.QRectF(0, 0, self.nchannels, self.range_period)
        self.rect4 = QtCore.QRectF(-90.0, 0, +180.0, self.range_period)
        self.rect5 = QtCore.QRectF(-self.velocity_period / 2, 0, self.velocity_period, self.range_period)

        # Defining timer
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(self.spinBox.value())

    def setInterval(self):
        self.timer.setInterval(self.spinBox.value())

    def updatePlot(self):
        data = read_frtm(self.results_files[self.n])  # number of the parametric setup

        # create 'raw_data' from the "RxSignal.frtm" file
        for i, ch in enumerate(data.all_data.keys()):
            self.raw_data[:, :, i] = data.all_data[ch].T # frequency points, chirp, channels

        # create range_arr --> ifft over the freq, over the channels (at a given chirp), let's choose chirp = 0
        range_arr = np.fft.ifft(self.raw_data[:, 0, :].T * signal.windows.hann(self.nfreq), axis=1, n=self.ovsp1 * self.nfreq)

        # create angle_arr --> fft over the channels, over ranges (we use range_arr array)
        angle_arr = np.fft.fft(range_arr[:, :].T, axis=1, n=self.nchannels * self.ovsp2)
        angle_arr = np.fft.fftshift(np.flipud(angle_arr), axes=1)

        # create doppler_velocity_arr (chirp vs range) --> fft over the freq. and fft over the chirp (at a given channel), let's choose channel = 0
        doppler_velocity_arr = np.fft.fft2(self.raw_data[:, :, 0].T, axes=(0, 1))
        doppler_velocity_arr = np.fft.fftshift(np.flipud(doppler_velocity_arr), axes=0)

        # Update Plot1
        x1 = np.linspace(0, self.range_period, self.ovsp1 * self.nfreq)
        y1 = 20 * np.log10(np.abs(range_arr[0].T))
        self.p1_item.setData(x1, y1)

        # Update Plot2
        z2 = 20 * np.log10(np.abs(range_arr))
        self.img2.setImage(z2)
        self.img2.setRect(self.rect2)

        # Update Plot3
        x3 = np.linspace(0, self.nfreq * self.range_resolution, self.ovsp1 * self.nfreq)
        y3 = np.linspace(-90.0, 90.0, self.nchannels * self.ovsp2)
        z3 = np.abs(angle_arr)
        cmap = plt.get_cmap('rainbow')
        rgba_img = cmap((z3 - np.min(z3)) / (np.max(z3) - np.min(z3)))
        self.p3.setData(x3 / np.max(x3), y3 / np.max(y3), z3 / np.max(z3), colors=rgba_img)

        # Update Plot4
        z4 = np.abs(angle_arr.T)
        self.img4.setImage(z4)
        self.img4.setRect(self.rect4)

        # Update Plot5
        z5 = np.abs(doppler_velocity_arr)
        self.img5.setImage(z5)
        self.img5.setRect(self.rect5)

        app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents)
        self.n = self.n + 1
        if self.n >= len(self.results_files):
            self.n = 0


if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    app.setStyle('Fusion')  # 'Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion'
    w = DesignerMainWindow()
    w.show()
    sys.exit(app.exec())
