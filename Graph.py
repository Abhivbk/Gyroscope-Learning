__author__ = 'Abhinav Kulkarni'


from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_values = []
y_values = []

index = count()

def animate(i):
    with open('orientation.txt', 'r') as f:
        roll = f.read()
    x_values.append(next(index))
    y_values.append(roll)
    print(x_values)
    print(y_values)
    plt.cla()
    plt.plot(x_values, y_values, marker='o')


ani = FuncAnimation(plt.gcf(), animate, 1000)


plt.tight_layout()
plt.show()