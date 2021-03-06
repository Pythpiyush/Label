# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'label2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import roslib
import rospy
from std_msgs.msg import String,Int32
from geometry_msgs.msg import Twist, Vector3
from math import radians
import os
import cv2
from PyQt5.QtGui import QImage,QPixmap,QColor
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QLabel
from cv_bridge import CvBridge
from sensor_msgs.msg import Image,CompressedImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer,QTime
import numpy as np
import time

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(974, 712)
        self.press = QtWidgets.QPushButton(Form)
        self.press.setGeometry(QtCore.QRect(420, 70, 131, 81))
        self.press.setObjectName("press")
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(130, 300, 311, 211))
        self.label1.setFrameShape(QtWidgets.QFrame.Box)
        self.label1.setText("")
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(560, 300, 341, 201))
        self.label2.setFrameShape(QtWidgets.QFrame.Box)
        self.label2.setText("")
        self.label2.setObjectName("label2")

        self.retranslateUi(Form)
        self.press.clicked.connect(Form.display)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.press.setText(_translate("Form", "Press"))


class Widget(QtWidgets.QWidget, Ui_Form):
    # rospy.Subscriber("/image_raw",Image,self.Receivedata,queue_size=1)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        # self.thread = MyThread()
        # self.thread.change_pixmap_signal.connect(self.displaynumb,QtCore.Qt.DirectConnection)
        # self.thread.start()
        self.press.clicked.connect(self.display)

    def display(self):
        os.system("rosrun uvc_camera uvc_camera_node &")

        #os.system("python talker.py &")

    def Receivedata(self, data):
        self.bridge = CvBridge()
        os.system("echo hello2")
        # bridge = CvBridge()
        os.system("echo yes i did it")
        # cv_image = self.bridge.imgmsg_to_cv2(data.data,"bgr8")
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.update_image(cv_image)

    def Receivedata2(self, data):
        self.bridge = CvBridge()
        os.system("echo hello2")
        # bridge = CvBridge()
        os.system("echo yes i did it")
        # cv_image = self.bridge.imgmsg_to_cv2(data.data,"bgr8")
        #cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "bgr8")
        self.update_image2(cv_image)

    def update_image2(self, cv_img):
        os.system("echo upimage")
        qt_img = self.convert_cv_qt(cv_img)
        self.label2.setPixmap(qt_img)


    def update_image(self, cv_img):
        os.system("echo upimage")
        qt_img = self.convert_cv_qt(cv_img)
        self.label1.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        os.system("echo conimage")
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 400)
        return QPixmap.fromImage(p)

    # os.system("echo hello2")
    # self.thread.run("hi")

    # connect its signal to the update_image slot

    # start the thread
    # def initialize(self):

    #def displaystr(self, data):
        #self.label1.setText(data.data)
        #rospy.sleep(1)

    #def displaynumb(self,data):
        #self.label2.setText(str(data.data))
        #rospy.sleep(1)


if __name__ == "__main__":
    import sys
    rospy.init_node('guinode', anonymous=True)
    app = QtWidgets.QApplication(sys.argv)
    Form = Widget()
    ui = Ui_Form()
    ui.setupUi(Form)
    #rospy.Subscriber('chatter', String, Form.displaystr, queue_size=1)
    #rospy.Subscriber('number', Int32, Form.displaynumb, queue_size=1)
    rospy.Subscriber('/image_raw', Image, Form.Receivedata, queue_size=1)
    rospy.Subscriber('/image_raw/compressed', CompressedImage, Form.Receivedata2, queue_size=1)
    #rospy.Subscriber('/image_raw', Image, Form.Receivedata, queue_size=1)
    Form.show()
    sys.exit(app.exec_())

