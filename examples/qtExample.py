# QT Example

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWidget(QtWidgets.QPushButton):
  def __init__(self):
    super(MyWidget,self).__init__()
    self.setText("Hello World!!")
    self.show()

def checkingGitHub():
  print ('Just Checking...')

def main():
  app = QtWidgets.QApplication(sys.argv)
  myWidget = MyWidget()
  sys.exit(app.exec_())

if __name__ == '__main__':
  checkingGitHub()
  main()