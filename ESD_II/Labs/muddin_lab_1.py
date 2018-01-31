#!/usr/bin/env python
# ==========================================
# @author Mosleh Uddin

# ==========================================
import sys, csv
from PyQt4 import QtGui, QtCore
from enum import Enum

BOARD_WIDTH = 50
BOARD_HEIGHT = 50

SINGLE_TURN_ANGLE = 45

ConfigParams = ['Width','Height','imgfile','cmdfile']

CarConfig = [
  {
    ConfigParams[0] : 4,
    ConfigParams[1] : 2,
    ConfigParams[2] : 'car1.png',
    ConfigParams[3] : 'encoder1.txt',
  },
]

# ==============================================================
class Car(QtGui.QGraphicsItem):
  def __init__(self, parent, arenaWidth, arenaHeight, carConfig):
    super(Car, self).__init__()

    self.carConfig = carConfig

    self.arenaWidth = arenaWidth
    self.arenaHeight = arenaHeight
    self.parent = parent

    self.carWidth = self.carConfig['Width']
    self.carHeight = self.carConfig['Height']

    # Place item in the center of the Arena
    self.setPos(self.arenaWidth/2,self.arenaHeight/2)

    # Accumulation of Car movement and turns
    self.forwardMovement = 0
    self.backwardMovement = 0
    self.carAngle = 0

    self.index = 0
    self.commands = self.fetchCommands();

    self.curRegion = 1
    self.x_dir = 1
    self.y_dir = 0
    self.curAngle = 0
    self.angMove = self.curAngle
    print (self.commands)
    # THE WAY!!
    # self.setRotation(315)

    # self.setX(self.x()+22)
    # self.setY(self.y()-22)

    # self.setRotation(135)

    self.x_pos = self.x() - 25.00
    self.y_pos = self.y() - 25.00

    print(self.x_pos)
    print(self.y_pos)

    # self.move()

  def boundingRect(self):
    return QtCore.QRectF(-self.carWidth/2, -self.carHeight/2,self.carWidth,self.carHeight)

  def paint(self, painter, option, widget):
    # painter.setBrush(QtGui.QColor(0,0,255))
    # painter.drawRect(-self.carWidth/2,-self.carHeight/2,self.carWidth,self.carHeight)
    # painter.setBrush(QtGui.QColor(255,255,1))
    # painter.drawRect(-self.carWidth/2,-self.carHeight/2,self.carWidth-1,self.carHeight)
    
    # Code for Image Placement
    self.pixmap = QtGui.QPixmap(self.carConfig['imgfile'])
    painter.drawPixmap(-self.carWidth/2, \
                    -self.carHeight/2, \
                    self.carWidth, \
                    self.carHeight, \
                    self.pixmap)

  def move(self):
    try:
      self.fr_com = self.commands['right'][self.index]
      self.fl_com = self.commands['left'][self.index]

      # self.setY(self.y() + 1)
      # print(self.y())
      # return 0

      if (self.fr_com > 0 or abs(self.fl_com) > 0):
        self.rem = abs(self.fr_com + self.fl_com)
        # if (self.rem == 0):
        #   self.setX(self.x() + (self.x_dir * self.fr_com))
        #   self.setY(self.y() + (self.y_dir * self.fr_com))

        # elif (self.rem > 0):
        # self.forMove = self.fr_com - self.rem
        if (self.fr_com > abs(self.fl_com)):
          self.angMove = ((45 * self.rem) + self.curAngle) % 360
          self.forMove = (self.fr_com + abs(self.fl_com)) - self.fr_com
          self.curAngle = self.angMove

          print ("1: FR > FL => " + str(self.fr_com) + " AND " + str(self.fl_com))
          print ("Angle => " + str(self.curAngle))
        elif (self.fr_com < abs(self.fl_com)):
          self.angMove = (abs((-45 * self.rem) + self.curAngle) % 360)
          self.forMove = (abs(self.fl_com) + self.fr_com) + self.fl_com
          self.curAngle = self.angMove 
          print ("2: FR > FL => " + str(self.fr_com) + " AND " + str(self.fl_com))
          print ("Angle => " + str(self.curAngle))
        else:
          self.forMove = self.fr_com
          print ("3: FR > FL => " + str(self.fr_com) + " AND " + str(self.fl_com))

        self.setX(self.x() + (self.x_dir * self.forMove))
        self.setY(self.y() + (self.y_dir * self.forMove))

        if (self.fr_com > abs(self.fl_com)):
          self.setRotation(-1 * self.angMove)
        elif (abs(self.fl_com) > self.fr_com):
          self.setRotation(self.angMove)

        if (self.angMove == 0):
          self.x_dir = 1
          self.y_dir = 0
        elif (self.angMove == 90):
          self.x_dir = 0
          self.y_dir = 1
        elif (self.angMove == 270):
          self.x_dir = -1
          self.y_dir = 0
        else:
          if (self.angMove > 0 and self.angMove < 90):
            self.x_dir = 1
            self.y_dir = -1
          elif (self.angMove > 90 and self.angMove < 180):
            self.x_dir = -1
            self.y_dir = 1
          elif (self.angMove > 180 and self.angMove < 270):
            self.x_dir = -1
            self.y_dir = -1
          elif (self.angMove > 270):
            self.x_dir = 1
            self.y_dir = 1

        self.index += 1

      else:
        self.index += 1

      return 0
    except IndexError:
      return 1

  def fetchCommands(self):
    commands = { }
    i = 0

    with open(self.carConfig['cmdfile'], 'rb') as csvfile:
      encoderReader = csv.reader(csvfile, delimiter = '\t', quotechar='|')
      for row in encoderReader:
        if (i != 0 and row != []):
          commands['l_dir'].append(-1 * int(row[0]))
          commands['left'].append(-1 * int(row[1]))
          commands['r_dir'].append(int(row[2]))
          commands['right'].append(int(row[3]))
        else:
          i += 1
          if (row != []):
            commands.update( {row[0]:[]} )
            commands.update( {row[1]:[]} )
            commands.update( {row[2]:[]} )
            commands.update( {row[3]:[]} )

    return commands

# ==============================================================
class Arena(QtGui.QGraphicsView):
  def __init__(self, parent):
    super(Arena, self).__init__()
    self.parent = parent
    self.scene = QtGui.QGraphicsScene(self)
    self.setScene(self.scene)

    self.arenaWidth = BOARD_WIDTH
    self.arenaHeight = BOARD_HEIGHT

    myFrame = self.scene.addRect(0,0,self.arenaWidth,self.arenaHeight)

    self.car = Car(self, self.arenaWidth, \
                         self.arenaHeight, \
                         CarConfig[0])
    self.scene.addItem(self.car)

    self.timer = QtCore.QBasicTimer()

  def startGame(self):
    self.status = 0
    self.car.setPos(25,25)
    self.car.setRotation(0)
    self.timer.start(1000, self)

  def timerEvent(self, event):
    if(self.status == 0):
      self.status = self.car.move()
    else:
      self.timer.stop()

  def resizeEvent(self, event):
    super(Arena, self).resizeEvent(event)
    self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

# ==============================================================
class FrontEnd(QtGui.QMainWindow):
  def __init__(self):
    super(FrontEnd,self).__init__()
    self.statusBar().showMessage('Ready')

    exitAction = QtGui.QAction('&Exit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit Application')
    exitAction.triggered.connect(QtGui.qApp.quit)

    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)

    self.hLayout = QtGui.QHBoxLayout()
    self.startButton = QtGui.QPushButton('Start')

    self.hLayout.addWidget(self.startButton)

    self.dockFrame = QtGui.QFrame()
    self.dockFrame.setLayout(self.hLayout)

    self.dock = QtGui.QDockWidget(self)
    self.dock.setWidget(self.dockFrame)
    self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dock)
    self.dock.setWindowTitle('Controls')

    self.setFocusPolicy(QtCore.Qt.StrongFocus)

    self.arena = Arena(self)

    self.hLayout = QtGui.QHBoxLayout()
    self.hLayout.addWidget(self.arena)

    self.frame = QtGui.QFrame(self)
    self.frame.setLayout(self.hLayout)

    self.setCentralWidget(self.frame)
    self.setWindowTitle('Vehicle Movement')
    self.showMaximized()
    self.show()

    self.startButton.clicked.connect(lambda: self.arena.startGame())

def main():
  app = QtGui.QApplication(sys.argv)
  app.setFont(QtGui.QFont('Helvetica', 10))

  frontEnd = FrontEnd()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()


