#!/usr/bin/env python3
# pip install filterpy scipy numpy

import numpy as np
from scipy.linalg import cholesky
from filterpy.kalman import UnscentedKalmanFilter as UKF

# Quadcopter motion model
def motion_model(x, dt):
    # Assuming a simple constant velocity model for the quadcopter
    F = np.array([[1, dt, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, dt],
                  [0, 0, 0, 1]])
    return np.dot(F, x)

# Measurement model (for simplicity, assume direct measurements of position)
def measurement_model(x):
    # Assuming we can directly measure the position (x, y)
    return x[[0, 2]]

# Process noise covariance matrix
Q = np.diag([0.1, 0.1, 0.1, 0.1])

# Measurement noise covariance matrix
R = np.diag([1.0, 1.0])

# Initial state
initial_state = np.array([0, 0, 0, 0])

# Initial state covariance matrix
P = np.diag([1.0, 1.0, 1.0, 1.0])

# Sigma points spreading parameter
alpha = 1e-3

# Create Unscented Kalman Filter
ukf = UKF(dim_x=4, dim_z=2, dt=0.1, fx=motion_model, hx=measurement_model, points=UKF.MerweScaledSigmaPoints(n=4, alpha=alpha, beta=2.0, kappa=0.0))

# Set initial state and covariance
ukf.x = initial_state
ukf.P = P

# Main loop
num_steps = 100
trajectory = []

for _ in range(num_steps):
    # Simulate motion
    ukf.predict()

    # Simulate measurement (add noise)
    measurement = measurement_model(ukf.x) + np.random.multivariate_normal(mean=np.zeros(2), cov=R)

    # Update with measurement
    ukf.update(measurement)

    # Save the estimated state
    trajectory.append(ukf.x.copy())

# Plot the results
import matplotlib.pyplot as plt

trajectory = np.array(trajectory)
plt.plot(trajectory[:, 0], trajectory[:, 2], label='Estimated Trajectory')
plt.title('Quadcopter Trajectory Estimation using UKF')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.show()
