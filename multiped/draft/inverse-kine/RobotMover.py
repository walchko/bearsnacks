from tkinter import *
import math as m
import matplotlib.pyplot as plt
import numpy as np
import serial
from mpl_toolkits.mplot3d import Axes3D
import serial.tools.list_ports
import time
"""
Created by: Klemen Štrajhar
Program deluje deluje samo na OS Windows. Ne vem kako se imenujejo serial porti na Linux ali OSX, 
da bi jih program avtomatsko zaznal.
Program bo deloval, ob trenutni postavitvi linkov robota. 
"""


#Incializacija seriala

ports = list(serial.tools.list_ports.comports())
port = []
ser = None
for p in ports:
    p = str(p)
    port.append(p)

for i in range(len(port)):
    if "ROBOTIS" in port[i]:
        a = port[i]
        real_port = a[0:4]
        print(real_port)
        ser = serial.Serial(real_port, baudrate=115200, timeout=0.05)


class Application(Frame):

    def createWidgets(self):
        """
        Naredi Tkinter GUI
        :return: void
        """
        # print(ser.readline().decode("ascii"))

        labelhello = Label(root, text="Welcome to leg controller")
        labelhello.grid(row=0, columnspan=6)

        label_coord1 = Label(root, text="X")
        label_coord1.grid(row=10, columnspan=2)
        label_coord1 = Label(root, text="Y")
        label_coord1.grid(row=10, columnspan=2, column=2)
        label_coord1 = Label(root, text="Z")
        label_coord1.grid(row=10, columnspan=2, column=4)

        self.xentry = Entry(root)
        self.xentry.insert(0,100)
        self.xentry.grid(row=11, columnspan=2)
        self.yentry = Entry(root)
        self.yentry.insert(0, 0)
        self.yentry.grid(row=11, columnspan=2, column=2)
        self.zentry = Entry(root)
        self.zentry.insert(0, -130)
        self.zentry.grid(row=11, columnspan=2, column=4)
        gumb_koord = Button(root, text="Poslji koordinate", command=self.moving)
        gumb_koord.grid(row=12, columnspan=6)

        label_coord1 = Label(root, text="  ")
        label_coord1.grid(row=13, columnspan=6)

        gumb_default = Button(root, text='Reset pozicije', command=self.reset)
        gumb_default.grid(row=14, columnspan=6)

        labelemp = Label(root, text=" ")
        labelemp.grid(row=15, columnspan=6)

        labelemp = Label(root, text="V primeru preobremenitve pritisni R za reset")
        labelemp.grid(row=16, columnspan=6)


        frame = Frame(root)
        root.bind("<Up>", self.Xup)
        root.bind("<Down>", self.Xdown)
        root.bind("<Left>", self.Yup)
        root.bind("<Right>", self.Ydown)
        root.bind("<Prior>", self.Zup)
        root.bind("<Next>", self.Zdown)
        root.bind("r",self.resetAlarm)
        frame.grid()

    def resetAlarm(self, event):
        print("Obremenitev resetirana")
        self.xb = 70
        self.yb = 0
        self.zb = -100
        self.movingX(method="alarm")
        # ser.write(data)


    def Xup(self, event):

        self.xb = self.xb + self.i
        self.movingX()

    def Xdown(self, event):
        self.xb = self.xb - self.i
        # if self.xb < 50:
        #     self.xb = 50
        self.movingX()

    def Yup(self, event):
        self.yb = self.yb + self.i
        self.movingX()

    def Ydown(self, event):
        self.yb = self.yb - self.i
        self.movingX()

    def Zup(self, event):
        self.zb = self.zb + self.i
        self.movingX()

    def Zdown(self, event):
        self.zb = self.zb - self.i
        self.movingX()

    def ForwardVectors(self, PA, PB,
                       l):  # PA je prve točka vektorja, PB je točka proti kateri gre vektor. l je dolžina vektorja.
        Vektor = -PA + PB
        Vektor_enotski = Vektor / m.sqrt(Vektor[0] ** 2 + Vektor[1] ** 2)
        Vektor_i = Vektor_enotski * l
        Pi = Vektor_i + PA
        return Pi

    def read_data(self, input):
        b = [index for index, value in enumerate(input) if value == "x"]
        kot1 = int(input[0:b[0]])
        kot2 = int(input[b[0] + 1:b[1]])
        kot3 = int(input[b[1] + 1:b[2]])
        kot4 = int(input[b[2] + 1:])
        return kot1, kot2, kot3, kot4

    def razdaljainkot(self, PA, PC, la, lb):
        dist = m.sqrt((PC[0] - PA[0]) ** 2 + (PC[1] - PA[1]) ** 2)
        try:
            q = m.acos((dist ** 2 - la ** 2 - lb ** 2) / (-2 * la * lb))
            return q
        except Exception:
            print("Izven delovnega območja")

    def angle_side(self, P_1, P_2, P_3, i):
        """
        Funkcija za izračun predznaka kota. 
        :return: predznak
        """
        predznak = 0
        k = (P_2[1] - P_1[1]) / (P_2[0] - P_1[0])
        fun_org = k * (P_3[0] - P_1[0]) + P_1[1]  # Dobimo vrednost funkcije, če za x vstavimo P_3[0]
        if i == 1:
            if k >= 0:
                if fun_org <= P_3[1]:
                    predznak = -1
                elif fun_org > P_3[1]:
                    predznak = 1
            elif k < 0:
                if fun_org < P_3[1]:
                    predznak = 1
                elif fun_org > P_3[1]:
                    predznak = -1

        if i == 2:
            if k >= 0:
                if fun_org <= P_3[1]:
                    predznak = -1
                elif fun_org > P_3[1]:
                    predznak = 1
            elif k < 0:
                if fun_org <= P_3[1]:
                    predznak = 1
                elif fun_org > P_3[1]:
                    predznak = 1
        return predznak

    def reset(self):  # Puts the robot to the starting position
        kot1 = 512
        kot2 = 300
        kot3 = 300
        kot4 = 300
        kot1H = (kot1 >> 8) & 255
        kot1L = kot1 & 255
        kot2H = (kot2 >> 8) & 255
        kot2L = kot2 & 255
        kot3H = (kot3 >> 8) & 255
        kot3L = kot3 & 255
        kot4H = (kot4 >> 8) & 255
        kot4L = kot4 & 255
        data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
        ser.write(data)



    def speedCalculate(self, KOT1, KOT2, time):
        delta = abs(KOT2 - KOT1)
        fi = (300 / 1023 * delta)  # Stopinje
        ang_velocity = m.radians(fi) / time
        rpm = ang_velocity / (2 * m.pi / 60)
        rpm_int = round(rpm / 0.111)
        return rpm_int

    def movingX(self, method = "normal"):
        """
        Izvede preračun za novo pozicijo in jo preko klica ser.write() pošlje na mikrokrmilnik.
        :return: 
        """
        time1 = time.clock()
        x = self.xb  # - self.ix
        y = self.yb
        z = self.zb  # - self.h
        if x ** 2 + y ** 2 + z ** 2 <= 67600:
            q2 = m.radians(int(90))
            q3 = m.radians(int(45))
            q4 = m.radians(int(45))

            P1i = np.array(([0, 0]))
            P2i = np.array([self.l1 * m.cos(q2), self.l1 * m.sin(q2)])
            P3i = np.array(
                [self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3), self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3)])
            P4i = np.array([self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3) + self.l3 * m.cos(q2 - q3 - q4),
                            self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3) + self.l3 * m.sin(q2 - q3 - q4)])

            G = np.array([m.sqrt(y ** 2 + x ** 2), z])
            P4ii = G
            for i in range(0, 100):
                P4i = G
                P3i = self.ForwardVectors(P4i, P3i, self.l3)
                P2i = self.ForwardVectors(P3i, P2i, self.l2)
                P1i = self.ForwardVectors(P2i, P1i, self.l1)

                P1ii = np.array([0, 0])
                P2ii = self.ForwardVectors(P1ii, P2i, self.l1)
                P3ii = self.ForwardVectors(P2ii, P3i, self.l2)
                P4ii = self.ForwardVectors(P3ii, G, self.l3)

                # Določitev novih vrednosti za novo zanko.
                P1i = P1ii
                P2i = P2ii
                P3i = P3ii
                P4i = P4ii
                # Izračun napake
                errx = abs(P4i[[0]] - G[[0]])
                errz = abs(P4i[[1]] - G[[1]])
                if errx < 0.01 and errz < 0.01:
                    break

            q1 = m.degrees(m.atan2(y, x))
            q2 = m.degrees(m.atan2(P2i[1], P2i[0]))
            q3 = 180 - m.degrees(self.razdaljainkot(P1i, P3i, self.l1, self.l2))
            q4 = 180 - m.degrees(self.razdaljainkot(P2i, P4i, self.l2, self.l3))

            if self.angle_side(P1i, P2i, P3i, 1) == 1:
                q3 = q3
            elif self.angle_side(P1i, P2i, P3i, 1) == -1:
                q3 = -q3

            if self.angle_side(P2i, P3i, P4ii, 2) == 1:
                q4 = q4
            elif self.angle_side(P2i, P3i, P4i, 2) == -1:
                q4 = -q4

            if q2 < 0:
                q3 = -q3

            self.q11 = q1
            self.q22 = q2
            self.q33 = q3
            self.q44 = q4

            kot1 = round(512 + (1023 / 300 * q1))
            kot2 = round(480 - (1023 / 300 * q2))
            kot3 = round(485 - (1023 / 300 * q3))
            kot4 = round(180 + (1023 / 300 * q4))
            print(kot1, kot2, kot3, kot4)
            kot1H = (kot1 >> 8) & 255
            kot1L = kot1 & 255
            kot2H = (kot2 >> 8) & 255
            kot2L = kot2 & 255
            kot3H = (kot3 >> 8) & 255
            kot3L = kot3 & 255
            kot4H = (kot4 >> 8) & 255
            kot4L = kot4 & 255
            if method == "normal":
                data = ([9, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
                ser.write(data)
            elif method == "alarm":
                data = ([7, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
                ser.write(data)
            print('Pozicija x: {}, y: {}, z: {}'.format(self.xb, self.yb, self.zb))
            print('Kot 1: {0:.3f}°, kot 2: {1:.3f}°, kot 3: {2:.3f}°, kot 4: {3:.3f}°'.format(q1, q2, q3, q4))

            # Odkomentiraj za dodatne informacije

            q1 = np.radians(q1)
            q2 = np.radians(q2)
            q3 = -np.radians(q3)
            q4 = -np.radians(q4)
            xa = (60 * np.cos(q2) + 60 * np.cos(q2 + q3) + 150 * np.cos(q2 + q3 + q4)) * m.cos(q1)
            za = 60 * np.sin(q2) + 60 * np.sin(q2 + q3) + 150 * np.sin(q2 + q3 + q4)
            ya = np.tan(q1) * xa
            print('Napake x: {0:.5f}, y:{1:.5f}, z:{2:.5f} [mm]'.format(abs(xa - self.xb), abs(ya - self.yb),
                                                                        abs(za - self.zb)))
            time2 = time.clock()
            cas = (time2 - time1) * 10 ** 3
            print("Čas za eksekucijo programa je %0.6f ms" % cas)
            print('Število iteracij {}'.format(i))
            print("  ")

        else:
            print("Koordinata izven dosegljivega območja", x ** 2 + y ** 2 + z ** 2)

    def moving(self):
        time1 = time.clock()
        x = int(self.xentry.get())  # -self.ix
        y = int(self.yentry.get())
        z = int(self.zentry.get())  # -self.h
        # Začetni pogoji
        self.xb = x
        self.xy = y
        self.zb = z
        if x ** 2 + y ** 2 + z ** 2 <= 67600:
            q2 = m.radians(int(90))
            q3 = m.radians(int(45))
            q4 = m.radians(int(45))

            P1i = np.array(([0, 0]))
            P2i = np.array([self.l1 * m.cos(q2), self.l1 * m.sin(q2)])
            P3i = np.array(
                [self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3), self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3)])
            P4i = np.array([self.l1 * m.cos(q2) + self.l2 * m.cos(q2 - q3) + self.l3 * m.cos(q2 - q3 - q4),
                            self.l1 * m.sin(q2) + self.l2 * m.sin(q2 - q3) + self.l3 * m.sin(q2 - q3 - q4)])

            G = np.array([m.sqrt(y ** 2 + x ** 2), z])
            P4ii = G
            for i in range(0, 100):
                P4i = G
                P3i = self.ForwardVectors(P4i, P3i, self.l3)
                P2i = self.ForwardVectors(P3i, P2i, self.l2)
                P1i = self.ForwardVectors(P2i, P1i, self.l1)

                P1ii = np.array([0, 0])
                P2ii = self.ForwardVectors(P1ii, P2i, self.l1)
                P3ii = self.ForwardVectors(P2ii, P3i, self.l2)
                P4ii = self.ForwardVectors(P3ii, G, self.l3)

                # Določitev novih vrednosti za novo zanko.
                P1i = P1ii
                P2i = P2ii
                P3i = P3ii
                P4i = P4ii
                # Izračun napake
                errx = abs(P4i[[0]] - G[[0]])
                errz = abs(P4i[[1]] - G[[1]])
                if errx < 0.01 and errz < 0.01:
                    break

            q1 = m.degrees(m.atan2(y, x))
            q2 = m.degrees(m.atan2(P2i[1], P2i[0]))
            q3 = 180 - m.degrees(self.razdaljainkot(P1i, P3i, self.l1, self.l2))
            q4 = 180 - m.degrees(self.razdaljainkot(P2i, P4i, self.l2, self.l3))

            if self.angle_side(P1i, P2i, P3i, 1) == 1:
                q3 = q3
            elif self.angle_side(P1i, P2i, P3i, 1) == -1:
                q3 = -q3

            if self.angle_side(P2i, P3i, P4ii, 2) == 1:
                q4 = q4
            elif self.angle_side(P2i, P3i, P4i, 2) == -1:
                q4 = -q4

            if q2 < 0:
                q3 = -q3

            # if q3>90:
            #     q4=-q4

            self.q11 = q1
            self.q22 = q2
            self.q33 = q3
            self.q44 = q4


            kot1 = round(512 + (1023 / 300 * q1))
            kot2 = round(480 - (1023 / 300 * q2))
            kot3 = round(485 - (1023 / 300 * q3))
            kot4 = round(180 + (1023 / 300 * q4))

            kot1H = (kot1 >> 8) & 255
            kot1L = kot1 & 255
            kot2H = (kot2 >> 8) & 255
            kot2L = kot2 & 255
            kot3H = (kot3 >> 8) & 255
            kot3L = kot3 & 255
            kot4H = (kot4 >> 8) & 255
            kot4L = kot4 & 255
            data = ([8, kot1H, kot1L, kot2H, kot2L, kot3H, kot3L, kot4H, kot4L])
            ser.write(data)
            print('Pozicija x: {}, y: {}, z: {}'.format(self.xb, self.yb, self.zb))
            print('Kot 1: {0:.3f}°, kot 2: {1:.3f}°, kot 3: {2:.3f}°, kot 4: {3:.3f}°'.format(q1, q2, q3, q4))
            # q1 = np.radians(q1)
            # q2 = np.radians(q2)
            # q3 = -np.radians(q3)
            # q4 = -np.radians(q4)
            # xa = (60 * np.cos(q2) + 60 * np.cos(q2 + q3) + 150 * np.cos(q2 + q3 + q4)) * m.cos(q1)
            # za = 60 * np.sin(q2) + 60 * np.sin(q2 + q3) + 150 * np.sin(q2 + q3 + q4)
            # ya = np.tan(q1) * xa
            # print('Napake x: {0:.5f}, y:{1:.5f}, z:{2:.5f} [mm]'.format(abs(xa - self.xb), abs(ya - self.yb),
            #                                                             abs(za - self.zb)))
            # print(np.sqrt(x ** 2 + y ** 2 + z ** 2))
            # time2 = time.clock()
            # cas = (time2 - time1) * 10 ** 3
            # print("Čas za eksekucijo programa je %0.6f ms" % cas)
            # print('Število iteracij {}'.format(i))
            # print("  ")


        else:
            print("Koordinata izven dosegljivega območja", x ** 2 + y ** 2 + z ** 2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # Spremenljivke
        self.xb = 70
        self.yb = 0
        self.zb = -100
        self.i = 10  # Velikost koraka premika [mm]
        self.h = 295
        self.ix = 50

        self.l1 = 60
        self.l2 = 60
        self.l3 = 150

        self.q11 = 0
        self.q22 = 90
        self.q33 = 45
        self.q44 = 45
        print("Started main thread")
        # Funkcije


        self.createWidgets()
        #self.readTorqueAlert()

        self.index = 0
        self.id = None








if __name__ == '__main__':

    root = Tk()
    app = Application(root)
    root.mainloop()

    ser.close()

