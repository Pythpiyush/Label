# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try3.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
#!env
from PyQt5 import QtCore, QtGui, QtWidgets
import roslib
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from math import radians
import os
import cv2
from PyQt5.QtGui import QImage,QPixmap,QColor
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QLabel
from cv_bridge import CvBridge
from sensor_msgs.msg import Image,CompressedImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer
import numpy as np


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 700)
        self.Image = QtWidgets.QPushButton(Form)
        self.Image.setGeometry(QtCore.QRect(140, 30, 89, 25))
        self.Image.setObjectName("Image")
        self.Display = QtWidgets.QLabel(Form)
        self.Display.setGeometry(QtCore.QRect(130, 110, 400, 400))
        self.Display.setFrameShape(QtWidgets.QFrame.Box)
        self.Display.setText("")
        self.Display.setObjectName("Display")

        self.retranslateUi(Form)
        self.Image.clicked.connect(Form.display)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Image.setText(_translate("Form", "Image"))




class Widget(QtWidgets.QWidget, Ui_Form):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.Image.clicked.connect(self.display)
	
    def display(self):
	    os.system("rosrun uvc_camera uvc_camera_node &")

    def Receivedata(self,data):
        self.bridge=CvBridge()
        os.system("echo hello2")
        #bridge = CvBridge()
        os.system("echo yes i did it")
        #cv_image = self.bridge.imgmsg_to_cv2(data.data,"bgr8")
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.update_image(cv_image)

    def update_image(self,cv_img):
        os.system("echo upimage")
        qt_img = self.convert_cv_qt(cv_img)
        self.Display.setPixmap(qt_img)
    
	
    def convert_cv_qt(self,cv_img):
        os.system("echo conimage")
        rgb_image=cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
        h,w,ch=rgb_image.shape
        bytes_per_line=ch*w
        convert_to_Qt_format=QtGui.QImage(rgb_image.data,w,h,bytes_per_line,QtGui.QImage.Format_RGB888)
        p=convert_to_Qt_format.scaled(400,400)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    import sys
    rospy.init_node('guinode',anonymous=True)
    rate=rospy.Rate(1)
    app = QtWidgets.QApplication(sys.argv)
    Form = Widget()
    ui = Ui_Form()
    ui.setupUi(Form)
    rospy.Subscriber('/image_raw', Image, Form.Receivedata,queue_size=1)
    rate.sleep()
    Form.show()
    sys.exit(app.exec_())

