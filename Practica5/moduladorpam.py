#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulador PAM
# Author: JuanSarmient_SergioUribe
# Copyright: JuanSarmient_SergioUribe
# Description: Modulador PAM
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class moduladorpam(gr.top_block, Qt.QWidget):

    def __init__(self, d=10, fs=100000, samp_rate=100000):
        gr.top_block.__init__(self, "Modulador PAM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulador PAM")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "moduladorpam")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.d = d
        self.fs = fs
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, d)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, fs, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self, 0), (self.blocks_multiply_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "moduladorpam")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_d(self):
        return self.d

    def set_d(self, d):
        self.d = d
        self.blocks_delay_0.set_dly(self.d)

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.analog_sig_source_x_0.set_frequency(self.fs)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)



def argument_parser():
    description = 'Modulador PAM '
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--d", dest="d", type=intx, default=10,
        help="Set Ancho del pulso [default=%(default)r]")
    return parser


def main(top_block_cls=moduladorpam, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(d=options.d)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
