import threading
import time
import sys
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt6.QtGui import QPixmap, QImage

from PyQt6 import QtWidgets, uic, QtCore


class Fork:
    def __init__(self, fork_id):
        self.fork_id = fork_id
        self.lock = threading.Lock()

    def pick_up(self):
        self.lock.acquire()

    def put_down(self):
        self.lock.release()

class Philosopher(threading.Thread):
    def __init__(self, id, left_fork, right_fork,ui):
        super().__init__()
        self.id = id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.ui=ui

    def run(self):
        while True:
            self.ui.update_label(f"Philosopher {self.id} is thinking.")
            time.sleep(2)  # Simulate thinking
            self.ui.update_label(f"Philosopher {self.id} is hungry.")
            self.left_fork.pick_up()
            self.ui.update_fork_status(self.id, True)  # Update fork image to picked up
            self.ui.update_label(f"Philosopher {self.id} picked up left fork.")
            self.right_fork.pick_up()
            self.ui.update_fork_status((self.id + 1) % 5, True)  # Update next philosopher's fork
            self.ui.update_label(f"Philosopher {self.id} picked up right fork and is eating.")
            time.sleep(2)  # Simulate eating
            self.right_fork.put_down()
            self.ui.update_fork_status((self.id + 1) % 5, False)  # Put down next philosopher's fork
            self.ui.update_label(f"Philosopher {self.id} put down right fork.")
            self.left_fork.put_down()
            self.ui.update_fork_status(self.id, False)  # Put down fork
            self.ui.update_label(f"Philosopher {self.id} put down left fork.")

class DiningPhilosophersApp(QtWidgets.QMainWindow):
    eating_signal = QtCore.pyqtSignal(int, bool)  # Signal to indicate eating status

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.forks = [Fork(i) for i in range(5)]
        self.philosophers = [Philosopher(i, self.forks[i], self.forks[(i + 1) % 5], self) for i in range(5)]
        self.start_philosophers()

class DiningPhilosophersGUI(QGraphicsView):
    def __init__(self, num_philosophers):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.num_philosophers = num_philosophers
        self.forks = [self.create_fork(i) for i in range(num_philosophers)]
        self.philosophers = [Philosopher(i, self.forks[i], self.forks[(i + 1) % num_philosophers]) for i in range(num_philosophers)]
        self.setFixedSize(800, 600)  # Set the window size
        self.draw_table()
        self.start_philosophers()

    def create_fork(self, id):
        return Fork(id)

    def draw_table(self):
        image_path = "E:\Dining Philosophers\pngegg.png"  # Replace with your image path
        pixmap = QPixmap(image_path)
        table = self.scene.addPixmap(pixmap)
        table.setPos(250, 150)  # Position the image at the center

    def start_philosophers(self):
        for philosopher in self.philosophers:
            philosopher.start()

def main():
    num_philosophers = 5
    app = QApplication(sys.argv)
    gui = DiningPhilosophersGUI(num_philosophers)
    gui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
