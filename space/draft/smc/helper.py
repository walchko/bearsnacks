import numpy as np
from matplotlib import pyplot as plt
from squaternion import Quaternion


def plotStates(ti,yi,qd):
    plt.figure(figsize=(20,5))

    plt.subplot(1,2,1)
    plt.plot(ti,yi[:,0], label="w")
    plt.plot(ti,yi[:,1], label="x")
    plt.plot(ti,yi[:,2], label="y")
    plt.plot(ti,yi[:,3], label="z")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Time [sec]")
    plt.title(f"$q_d$: {qd:.3f}");

    plt.subplot(1,2,2)
    plt.plot(ti,yi[:,4], label="$\omega_x$")
    plt.plot(ti,yi[:,5], label="$\omega_y$")
    plt.plot(ti,yi[:,6], label="$\omega_z$")
    plt.grid(True)
    plt.xlabel("Time [sec]")
    plt.title("Attitude Rates [rad/sec]")
    plt.legend();

def plotControl(ti, ui, err, errdot, step, h=None):
    plt.figure(figsize=(20,5))
    
    num = 2 if h is None else 3

    plt.subplot(1,num,1)
    ts = np.sum(np.abs(ui))*step
    plt.plot(ti,ui[:,0], label="x")
    plt.plot(ti,ui[:,1], label="y")
    plt.plot(ti,ui[:,2], label="z")
    plt.grid(True)
    plt.xlabel("Time [sec]")
    plt.title(f"Torque ({ts:.2f}) [N-m]")
    plt.legend();

    plt.subplot(1,num,2)
    ee = [e[1:]/e[0] for e in err]
    plt.plot(errdot,ee)
    plt.xlabel("Error Rate [rad/sec]")
    plt.ylabel("Error [$\mathbb{Im}(q)$]")
    plt.title("Phase Plane Error")
    plt.grid(True);
    
    if num == 3:
        hh = np.sum(np.abs(h))*step
        plt.subplot(1,num,3)
        plt.plot(ti,h[:,0], label="hx")
        plt.plot(ti,h[:,1], label="hy")
        plt.plot(ti,h[:,2], label="hz")
        plt.grid(True)
        plt.legend()
        plt.xlabel("Time [sec]")
        plt.title(f"Wheel Momentum ({hh:.2f}) [N-m-s]");