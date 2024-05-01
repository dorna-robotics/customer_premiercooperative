# Installation
There is a 3D camera (stereo camera) connected to the probe. 

# Kinematics
The probe has 2 main joints. One moves the probe left and right on a circle, and another one makes the probe goes up and down. We call these two joints `p0` and `p1`. The speed of each joint `vp0` and `vp1` is also known an defined as `vp0` and `vp1`, respectively.

# Frame
As shown here, there are two main frames, camera and probe frames.  
A point `(x, y, z)` in the camera frame is translates to `(x, y.cos(t)-z.sin(t), y.sin(t)+z.cos(t)-d)` in probe frame. Where `t` and `d` are fixed values.

# Selecting `p1`
Notice that when `p0` is fixed there will be a unique touching point of the grain surface and the probe.


# Navigation
The camera is mounted on the probe head, and looking down.
A narrow window is defined such that when the probe goes down then it will touch the surface on this narrow window.
For example if the 