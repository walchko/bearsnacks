---
title: Complementary Filter
image: "https://i.pinimg.com/564x/af/6c/f2/af6cf22d6c851eae0c623fafd0751efa.jpg"
image-height: "300px"
date: 31 Aug 2020
---

Choosing $\alpha$?

$$
\alpha = \tau / (\tau + dt) \\
dt = 1/f_s
$$

where $\tau$ is the desired time constant (how fast you want the readings to respond) 
and $f_s$ is your sampling frequency. This equation is derived from filter/control theory

# References

- github: [IMU tools for ROS](https://github.com/ccny-ros-pkg/imu_tools)
- [Keeping a Good Attitude: A Quaternion-Based Orientation Filter for IMUs and MARGs](https://www.mdpi.com/1424-8220/15/8/19302)
- [Complementary filter design](https://gunjanpatel.wordpress.com/2016/07/07/complementary-filter-design/)
- MIT: [16.333: Lecture 15, Complementary filtering](https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-333-aircraft-stability-and-control-fall-2004/lecture-notes/lecture_15.pdf)
