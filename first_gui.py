#!/usr/bin/env python




import sys
import time
from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget



class SampleWindow(QWidget):
    """ Main Window Class"""

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Sample Window")
        self.setGeometry(300, 300, 200, 150)
        self.setMinimumHeight(100)
        self.setMinimumWidth(250)
        self.setMaximumHeight(500)
        self.setMaximumWidth(800)

    def setButton(self):
        """Function to add a quit button"""

        myButton=QPushButton("QUIT", self)
        myButton.move(50,100)
        myButton.clicked.connect(self.quitter)

    def quitter(self):
        """Function to confirm before quittin"""

        userInfo=QMessageBox.question(self, 'Confirmation', "This will quit the application.  Continue?", QMessageBox.Yes | QMessageBox.No)

        if userInfo==QMessageBox.Yes:
            print "answer yes"
            myApp.quit()
        else:
            print "answer no"
            pass

    def center(self):
        """Function to center the application window"""

        qRect=self.frameGeometry()
        centerPoint=QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def setAboutButton(self):
        """Function to set About Button"""

        self.aboutButton=QPushButton('About', self)
        self.aboutButton.move(100, 100)
        self.aboutButton.clicked.connect(self.showAbout)

    def showAbout(self):
        """Function to show About box"""

        QMessageBox.about(self.aboutButton, "About PySide", "PySide is a cross-platform tool for generating GUI programs")




if __name__ == '__main__':

    try:
        myApp=QApplication(sys.argv)
        myWindow=SampleWindow()
        myWindow.setWindowTitle("Sample Window")
        myWindow.setButton()
        myWindow.setAboutButton()
        myWindow.center()
        myWindow.show()
        myApp.exec_()
  #      time.sleep(1)
  #      myWindow.resize(300, 300)
  #      myWindow.setWindowTitle("Sample Window Resized")
  #      myWindow.repaint()
  #      time.sleep(5)
  #      myWindow.resize(500, 800)
  #      myWindow.setWindowTitle("Sample Window Resized Again")
  #      myWindow.repaint()
  #      myApp.exec_()
        sys.exit(0)
    except NameError:
        print ("name error: ", sys.exc_info()[1])
    except SystemExit:
        print ("closing window...")
    except Exception:
        print (sys.exc_info()[1])

