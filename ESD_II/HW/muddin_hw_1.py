# ==========================================
# @author Mosleh Uddin
# @date   01/17/2018
# @title  Homework 1 - ESD II
#
# @description Program using PyQt4
# ==========================================

import sys, random
from PyQt4 import QtGui, QtCore

class Crisp(QtGui.QMainWindow):
  def __init__(self):
    super(Crisp, self).__init__()
    self.statusBar().showMessage('Ready')
    
    exitAction = QtGui.QAction('&Exit', self)        
    exitAction.setShortcut('Ctrl+Q')
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(QtGui.qApp.quit)
    
    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(exitAction)    
    
    self.hLayout = QtGui.QHBoxLayout()
    self.startButton = QtGui.QPushButton("Start")  

    self.changeColor = QtGui.QPushButton("Change Color")
    self.reduceSpeed = QtGui.QPushButton("Reduce Speed")
    self.increaseSpeed = QtGui.QPushButton("Increase Speed")

    self.hLayout.addWidget(self.startButton)  
    self.hLayout.addWidget(self.changeColor)
    self.hLayout.addWidget(self.reduceSpeed)
    self.hLayout.addWidget(self.increaseSpeed)

    
    self.dockFrame = QtGui.QFrame()
    self.dockFrame.setLayout(self.hLayout)    
    
    self.dock = QtGui.QDockWidget(self)
    self.dock.setWidget(self.dockFrame)
    self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dock)
    self.dock.setWindowTitle("Controls")

    self.setFocusPolicy(QtCore.Qt.StrongFocus) 
 
    self.board = Board(self)
    self.vLayout = QtGui.QVBoxLayout()    
    self.vLayout.addWidget(self.board)
    
    self.frame = QtGui.QFrame(self)
    self.frame.setLayout(self.vLayout)

    self.setCentralWidget(self.frame)
    self.setWindowTitle("Crisp Bounce") 
    self.showMaximized()
    self.show()
    
    #styleFile ="styleSheet.txt"
    #with open(styleFile,"r") as fh:
    #  self.setStyleSheet(fh.read())
    
    #self.board.startGame()
    self.changeColor.clicked.connect(lambda: self.board.setColor())
    self.increaseSpeed.clicked.connect(lambda: self.board.increaseBallSpeed())
    self.reduceSpeed.clicked.connect(lambda: self.board.decreaseBallSpeed())


    self.startButton.clicked.connect(lambda: self.board.startGame()) 

class Ball(QtGui.QGraphicsItem):
  def __init__(self,parent,boardWidth,boardHeight):
    super(Ball, self).__init__()     
    self.color = QtGui.QColor(0,0,255)
    self.xVel = 10
    self.yVel = 5
    self.ballWidth = 30
    self.ballHeight = 30
    self.boardWidth = boardWidth
    self.boardHeight = boardHeight
    self.parent = parent
     
  def boundingRect(self):
    return QtCore.QRectF(-self.ballWidth/2,-self.ballHeight/2,self.ballWidth,self.ballHeight)
      
  def paint(self, painter, option, widget):
    painter.setBrush(self.color)
    painter.drawEllipse(-self.ballWidth/2,-self.ballHeight/2,self.ballWidth,self.ballHeight)       
     
  def reflectX(self):
    self.xVel = self.xVel * -1
      
  def reflectY(self):
    self.yVel = self.yVel * -1   
      
  def move(self):
    self.setX(self.x() + self.xVel)
    if (self.x() >= self.boardWidth - self.ballWidth/2):
      #return 2
      self.reflectX()
    elif (self.x() <= self.ballWidth/2):
      #return 1
      self.reflectX()
  
    self.setY(self.y() + self.yVel)
    if (self.y() >= self.boardHeight - self.ballHeight/2):
      self.reflectY()
    elif (self.y() <= self.ballHeight/2):
      self.reflectY()

    return 0

  def setColor(self):
    self.color = QtGui.QColor(random.randint(0,255), \
                              random.randint(0,255), \
                              random.randint(0,255))

  def decreaseBallSpeed(self):
    if(self.yVel != 0):
      if(self.yVel < 1):
        self.yVel += 1
      else:
        self.xVel -= 1

      if(self.xVel < 1):
        self.xVel += 1
      else:
        self.xVel -= 1;
    else:
      self.xVel = 0

  def increaseBallSpeed(self):
    if(self.xVel != 0 and self.xVel <= 100):
      if(self.yVel < 1):
        self.yVel -= 1
      else:
        self.xVel += 1

      if(self.xVel < 1):
        self.xVel -= 1
      else:
        self.xVel += 1;
    elif (self.xVel == 0):
      self.xVel = 6
      self.yVel = 1

class Board(QtGui.QGraphicsView):   
  def __init__(self,parent):
    super(Board, self).__init__()
    self.parent = parent
    self.scene = QtGui.QGraphicsScene(self)
    self.setScene(self.scene)
    
    self.boardWidth = 1000
    self.boardHeight = 1000    
    
    # effectively sets the logical scene coordinates from 0,0 to 1000,1000
    myFrame = self.scene.addRect(0,0,self.boardWidth,self.boardHeight) 

    # self.leftPaddle = Paddle(self.boardWidth,self.boardHeight)
    # self.rightPaddle = Paddle(self.boardWidth,self.boardHeight)
    self.ball = Ball(self,self.boardWidth,self.boardHeight)
    
    self.scene.addItem(self.ball)
 
    self.timer = QtCore.QBasicTimer()
    self.ball.setPos(500,500)
  
  def setColor(self):
    self.ball.setColor()

  def increaseBallSpeed(self):
    self.ball.increaseBallSpeed()

  def decreaseBallSpeed(self):
    self.ball.decreaseBallSpeed()

  def startGame(self):
    self.status = 0
    self.ball.setPos(500,500)
    self.timer.start(17, self)   

  def timerEvent(self, event): 
    if (self.status == 0):
      self.status = self.ball.move()
    else:
      self.timer.stop()
        
  def resizeEvent(self, event):
    super(Board, self).resizeEvent(event)
    self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio) 
       
def main():
  app = QtGui.QApplication(sys.argv)
  app.setFont(QtGui.QFont("Helvetica", 10))  
  crisp = Crisp()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()