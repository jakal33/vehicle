import tkinter as tk
import random


WIDTH = 800
HEIGHT = 600

CAR_WIDTH = 50
CAR_HEIGHT = 90

class ADASSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("ADAS Vehicle Simulation")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="gray20")
        self.canvas.pack()

        # Road
        self.road_left = 250
        self.road_right = 550

        # Vehicle state
        self.speed = 80.0  # km/h
        self.max_speed = 120
        self.acceleration = 0

        # Car position
        self.car_x = WIDTH // 2
        self.car_y = HEIGHT - 120

        # Create car
        self.car = self.canvas.create_rectangle(
            self.car_x - CAR_WIDTH // 2,
            self.car_y - CAR_HEIGHT // 2,
            self.car_x + CAR_WIDTH // 2,
            self.car_y + CAR_HEIGHT // 2,
            fill="dodgerblue"
        )

        # Obstacle
        self.obstacle = None
        self.obstacle_y = -100
        self.obstacle_speed = 5

        # ADAS
        self.warning_distance = 200
        self.brake_distance = 120

        # UI labels
        self.speed_label = tk.Label(root, font=("Arial", 12))
        self.speed_label.pack()

        self.distance_label = tk.Label(root, font=("Arial", 12))
        self.distance_label.pack()

        self.status_label = tk.Label(root, font=("Arial", 14, "bold"))
        self.status_label.pack()

        # Controls
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Accelerate",
                  command=self.accelerate).grid(row=0, column=0)

        tk.Button(frame, text="Brake",
                  command=self.brake).grid(row=0, column=1)

        tk.Button(frame, text="Reset Speed",
                  command=self.reset_speed).grid(row=0, column=2)

        self.draw_road()
        self.spawn_obstacle()

        self.update()

    def draw_road(self):
        self.canvas.create_rectangle(
            self.road_left, 0,
            self.road_right, HEIGHT,
            fill="gray40",
            outline=""
        )

        for y in range(0, HEIGHT, 40):
            self.canvas.create_line(
                WIDTH // 2,
                y,
                WIDTH // 2,
                y + 20,
                fill="white",
                width=4
            )

    def spawn_obstacle(self):
        if self.obstacle:
            self.canvas.delete(self.obstacle)

        self.obstacle_y = -100

        self.obstacle = self.canvas.create_rectangle(
            WIDTH // 2 - 25,
            self.obstacle_y,
            WIDTH // 2 + 25,
            self.obstacle_y + 60,
            fill="red"
        )

    def accelerate(self):
        self.speed = min(self.max_speed, self.speed + 10)

    def brake(self):
        self.speed = max(0, self.speed - 15)

    def reset_speed(self):
        self.speed = 80

    def update_obstacle(self):
        movement = max(2, self.speed / 10)

        self.obstacle_y += movement

        self.canvas.coords(
            self.obstacle,
            WIDTH // 2 - 25,
            self.obstacle_y,
            WIDTH // 2 + 25,
            self.obstacle_y + 60
        )

        if self.obstacle_y > HEIGHT:
            self.spawn_obstacle()

    def adas_logic(self):
        obstacle_bottom = self.obstacle_y + 60

        distance = self.car_y - obstacle_bottom

        self.distance_label.config(
            text=f"Distance: {max(0, int(distance))} px"
        )

        # Forward Collision Warning
        if distance < self.warning_distance:
            self.status_label.config(
                text="⚠ Forward Collision Warning",
                fg="orange"
            )
        else:
            self.status_label.config(
                text="Normal Driving",
                fg="green"
            )

        # Automatic Emergency Braking
        if distance < self.brake_distance:
            self.speed -= 2.5

            if self.speed < 0:
                self.speed = 0

            self.status_label.config(
                text="Automatic Emergency Braking",
                fg="red"
            )

        # Collision
        if distance <= 0:
            self.speed = 0

            self.status_label.config(
                text="💥 COLLISION",
                fg="white",
                bg="red"
            )

    def update(self):
        self.update_obstacle()
        self.adas_logic()

        self.speed_label.config(
            text=f"Vehicle Speed: {self.speed:.1f} km/h"
        )

        self.root.after(50, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = ADASSimulator(root)
    root.mainloop()
