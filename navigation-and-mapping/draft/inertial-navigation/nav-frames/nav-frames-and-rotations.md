---
title: Navigation Frames and Rotations
---

## Euler

$$
x^G = R_{S}^G x^S = R_z R_y R_x x^S
$$

where G refers to the global navigation frame and S is the sensor frame on the system.

- yaw (or heading): [-180, 180]
- pitch: [-90, 90]
- roll: [-180, 180]

## Quaternions

$$
x^G = q_{GS} \circ x^S \circ q_{GS}^* = q_{GS} \circ x^S \circ q_{SG} 
$$

## Nav

```python
enu2ned = np.array([
    [0,1,0],
    [1,0,0],
    [0,0,-1]
])
```
