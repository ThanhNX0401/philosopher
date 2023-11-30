import threading
import time
import tkinter as tk

class Philosopher(threading.Thread):
    def __init__(self, name, left_chopstick, right_chopstick, gui):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.state = "Thinking"
        self.running = True
        self.gui = gui

    def run(self):
        while self.running:
            time.sleep(1)  # Placeholder for eating/thinking time
            if self.state == "Eating":
                self.eat()

    def eat(self):
        with self.left_chopstick, self.right_chopstick:
            print(f"{self.name} is Eating")
            self.gui.update_philosopher_state(self.name, self.state)
            time.sleep(1)  # Simulating eating time
        self.state = "Thinking"
        print(f"{self.name} is Thinking")
        self.gui.update_philosopher_state(self.name, self.state)

    def stop(self):
        self.running = False


class DiningPhilosophersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dining Philosophers")
        self.philosophers = []
        self.chopsticks = [threading.Lock() for _ in range(5)]
        self.create_interface()

    def create_interface(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Draw the table
        self.canvas.create_oval(50, 50, 350, 350, outline='black')

        # Draw the chopsticks
        for angle in range(72, 361, 72):
            x1 = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            y1 = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            x2 = x1 + 30 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            y2 = y1 - 30 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            self.canvas.create_line(x1, y1, x2, y2, fill='black', width=3)

        # Draw the plates
        for angle in range(0, 360, 72):
            x = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            y = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='white', outline='black')

        # Draw the philosophers
        for angle in range(0, 360, 72):
            x = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            y = 200 + 150 * (3 ** 0.5) * (1/2) * (1 - (angle % 360) // 360)
            self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, outline='black')

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack()

    def start_simulation(self):
        for i in range(5):
            philosopher = Philosopher(f"Philosopher {i+1}", self.chopsticks[i], self.chopsticks[(i+1) % 5], self)
            self.philosophers.append(philosopher)
            self.create_philosopher_window(philosopher)

    def create_philosopher_window(self, philosopher):
        window = tk.Toplevel(self.root)
        window.title(philosopher.name)
        window.geometry("200x150")  # Enlarged window size
        state_label = tk.Label(window, textvariable=tk.StringVar(value=philosopher.state))
        state_label.pack()

        id_label = tk.Label(window, text=f"ID: {philosopher.name}")
        id_label.pack()

        def toggle_state():
            if philosopher.state == "Eating":
                philosopher.state = "Thinking"
            else:
                philosopher.state = "Eating"
                philosopher.start()  # Start eating when toggled
            state_label.config(text=philosopher.state)
            self.update_philosopher_state(philosopher.name, philosopher.state)

        state_button = tk.Button(window, text="Toggle State", command=toggle_state)
        state_button.pack()

        window.protocol("WM_DELETE_WINDOW", philosopher.stop)

        philosopher.gui_window = window

    def update_philosopher_state(self, philosopher_name, state):
        for philosopher in self.philosophers:
            if philosopher.name == philosopher_name:
                philosopher.gui_window.children["!label"].config(text=state)

    def stop_simulation(self):
        for philosopher in self.philosophers:
            philosopher.stop()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = DiningPhilosophersGUI(root)
    root.mainloop()
