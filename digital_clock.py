#!/usr/bin/env python

import sys
from PySide.QtCore import QDateTime, QTimer, SIGNAL
from PySide.QtGui import QApplication, QWidget, QLCDNumber


class MyTimer(QWidget):
    """Main window class for the timer"""

    def __init__(self):
        """constructor function"""
        title="my digital clock"

        QWidget.__init__(self)
        self.setWindowTitle(title)
        timer=QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.updtTime)
        self.myTimeDisplay=QLCDNumber(self)
        self.myTimeDisplay.setSegmentStyle(QLCDNumber.Filled)
        self.myTimeDisplay.setDigitCount(8)
        self.myTimeDisplay.resize(500, 150)
        timer.start(1000)

    def updtTime(self):
        """Function to update current time"""

        currentTime=QDateTime.currentDateTime().toString("hh:mm:ss")
        self.myTimeDisplay.display(currentTime)

if __name__ == "__main__":
    try:
        myApp=QApplication(sys.argv)
        myWindow=MyTimer()
        myWindow.show()
        myApp.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print ("Closing Window...")
    except Exception:
        print (sys.exc_info()[1])


