import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLCDNumber
from PyQt6.QtCore import QTimer


# class that creates the Pomodoro interface and functions
class PomodoroApp(QWidget):

   # define constructor to create the interface by building on parent class QWidget
   def __init__(self):
       super().__init__()

       # set window title to Pomodoro Timer
       self.setWindowTitle("Pomodoro Timer")

        """ set work time (30 min), break time (5 min), and a long break time (15 min)"""
       self.work = 30 * 60  # 25 minutes in seconds
       self.breakTime = 5 * 60  # 5 minutes in seconds
       self.longBreak = 15 * 60  # 15 minutes in seconds
       self.now = self.work

       # indicates if break time has been reached
       self.is_break = False

       # counts the amount of pomodoro sessions taken
       self.sessionCount = 0

       # creates timer using QTimer 
       self.timer = QTimer(self)

       # at end of intervals, update the timer
       self.timer.timeout.connect(self.update)

       # used for digital clock (QLCDNumber) 
       self.time_display = QLCDNumber()
       # up to 7 digit time
       self.time_display.setDigitCount(7)
       # set to 30 min timer
       self.time_display.display("30:00")

       # creates a start button that when clicked will start the timer 
       self.startBut = QPushButton("Start")
       self.startBut.clicked.connect(self.start)

       # creates a pause button that when clicked will pause the timer 
       self.pauseBut = QPushButton("Pause")
       self.pauseBut.clicked.connect(self.pause)
       self.pauseBut.setEnabled(False)

       # creates a reset button that when clicked will restart the timer to 30 min
       self.resetBut = QPushButton("Reset")
       self.resetBut.clicked.connect(self.reset)

       # QVBoxLayout allows vertical positioning of items, so position 
       # the time, start, pause, and reset button
       # add the layout to the main window and center the window
       layout = QVBoxLayout()
       layout.addWidget(self.time_display)
       layout.addWidget(self.startBut)
       layout.addWidget(self.pauseBut)
       layout.addWidget(self.resetBut)
       self.setLayout(layout)
       self.center()

   # centers the window 
   def center(self):
       screen = QApplication.primaryScreen()  # get the display screen
       screenGeometry = screen.geometry()  # get screen size and position
       windowGeometry = self.geometry()  # get window size and position

       # find the center position and set the center position of the screen to the window
       x = (screenGeometry.width() - windowGeometry.width()) // 2
       y = (screenGeometry.height() - windowGeometry.height()) // 2

       self.setGeometry(x, y, windowGeometry.width(), windowGeometry.height())

   # define a start function to allow user to start timer 
   # emit timeout signal every 1000ms(second) to effectively trigger decrease in time
   # don't let user be able to start the timer again
   def start(self):
       self.timer.start(1000)
       self.startBut.setEnabled(False)
       self.pauseBut.setEnabled(True)

   # define a pause function to allow user to pause 
   # let user be able to start timer, but not pause after pressing pause
   def pause(self):
       self.timer.stop()
       self.startBut.setEnabled(True)
       self.pauseBut.setEnabled(False)

   # define a reset button to pause the timer, reset to 30 min
   # reset is_break to false to signify not a break
   # reset sessionCount because no sessions recorded, update display 
   def reset(self):
       self.pause()
       self.now = self.work
       self.is_break = False
       self.sessionCount = 0
       self.update_display()

   # the update function updates the time by decreasing timer by 1 second
   # changes into next minute if seconds < 0 (goes to 59) 
   def update(self):
       self.now -= 1
       if self.now == 0:
           self.switch()
       self.update_display()

   # swtich from break to working session by setting to 30 min, reset is_break to false
   # increase session count by 1
   # take a long break every 3 sessions, else regular break session
   def switch(self):
       if self.is_break:
           self.now = self.work
           self.is_break = False
           self.sessionCount += 1
       else:
           if self.sessionCount % 3 == 0:
               self.now = self.longBreak
           else:
               self.now = self.breakTime
           self.is_break = True

   # return the minutes and seconds to display on screen in 2 digit format (MM:SS) 
   def update_display(self):
       minutes, seconds = divmod(self.now, 60)
       self.time_display.display(f"{minutes:02}:{seconds:02}")

# only executes when executed directly, not imported code
# create window to be able to display the timer
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = PomodoroApp()
   window.show()
   sys.exit(app.exec())
