import serial
import serial.tools.list_ports
from tkinter import *
from time import sleep
import numpy as np
import math as m
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Created by: Klemen Štrajhar


class Application():
    def __init__(self):
        self.connect_serial()
        self.readSer()

        self.l1 = 60
        self.l2 = 60
        self.l3 = 150
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

    def connect_serial(self):
        """
        Vzpostavi povezavo s portom. Samodejno najde port na katerega je priključen openCM.
        :return: void
        """
        ports = list(serial.tools.list_ports.comports())
        port = []
        for p in ports:
            p = str(p)
            port.append(p)

        for i in range(len(port)):
            if "ROBOTIS" in port[i]:
                a = port[i]
                real_port = a[0:4]
                print(real_port)
                self.ser = serial.Serial(real_port, baudrate=57600, timeout=1)

    def close_serial(self):
        """
        Zapre serijsko povezavo ob zaprtju GUI
        :return: void
        """
        self.ser.close()

    def readSer(self):
        # self.ser.read()
        #plt.ion()  # Enable interactive mode
        fig = plt.figure()
        #gs1 = gridspec.GridSpec(2, 1)
        axes = fig.gca(projection="3d")
        axes.set_xlim(-50, 200)
        axes.set_ylim(-100, 100)
        axes.set_zlim(-200,200)
        axes, = axes.plot([], [], [])

        while 1:
            # incoming_Stream = self.ser.readline().decode("utf8")
            # a = self.read_angles(incoming_Stream)
            a = None

            X, Y, Z = self.draw_robot(a)
            #axes.plot(X,Y,Z)

            axes.set_data(X,Y)
            axes.set_3d_properties(Z)

            plt.draw()
            plt.pause(0.01)

    def read_angles(self, input):

        input = [(i,1023) for i in range(6)]

        b = [index for index, value in enumerate(input) if value == "x"]
        kot1 = int(input[0:b[0]])
        kot2 = int(input[b[0] + 1:b[1]])
        kot3 = int(input[b[1] + 1:b[2]])
        kot4 = int(input[b[2] + 1:])
        return kot1, kot2, kot3, kot4

    def draw_robot(self, angle_array):
        l1 = l2 = 60
        l3 = 150

        q1 = (angle_array[0] - 512) / 1023 * 300
        q2 = (480 - angle_array[1]) / 1023 * 300
        q3 = (485 - angle_array[2]) / 1023 * 300
        q4 = (angle_array[3] - 180) / 1023 * 300

        q1 = m.radians(q1)
        q2 = m.radians(q2)
        q3 = -m.radians(q3)
        q4 = -m.radians(q4)

        x1 = 0
        x2 = (l1 * m.cos(q2))
        x3 = (l1 * m.cos(q2) + l2 * m.cos(q2 + q3))
        x4 = (l1 * m.cos(q2) + l2 * m.cos(q2 + q3) + l3 * m.cos(q2 + q3 + q4))

        z1 = 0
        z2 = l1 * m.sin(q2)
        z3 = l1 * m.sin(q2) + l2 * m.sin(q2 + q3)
        z4 = l1 * m.sin(q2) + l2 * m.sin(q2 + q3) + l3 * m.sin(q2 + q3 + q4)

        y1 = 0
        y2 = x2 * m.sin(q1)
        y3 = x3 * m.sin(q1)
        y4 = x4 * m.sin(q1)

        x1 = 0
        x2 = x2 * m.cos(q1)
        x3 = x3 * m.cos(q1)
        x4 = x4 * m.cos(q1)

        X = np.array([x1, x2, x3, x4])
        Y = np.array([y1, y2, y3, y4])
        Z = np.array([z1, z2, z3, z4])
        #print(m.sin(q1)*100, y2, y3, y4)
        #print(m.degrees(q1),x4,y4)
        return X, Y, Z


app = Application()

app.close_serial()
