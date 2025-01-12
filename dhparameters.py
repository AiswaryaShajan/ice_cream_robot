import numpy as np

def dh_transform(theta, d, a, alpha):
    theta = np.deg2rad(theta)
    alpha = np.deg2rad(alpha)
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# DH parameters for Epson VT6 with corrected values
dh_params = [
    [0, 412.0, 0.0, 0.0],
    [-90, 0.0, 100.0, -90.0],
    [0, 0.0, 420.0, 0.0],
    [0, 400.0, 0.0, -90.0],
    [0, 0.0, 0.0, 90.0],
    [0, 80.0, 0.0, -90.0]
]

# Joint angles (example values)
joint_angles = [30, 45, 60, 90, 45, 30]

# Compute the overall transformation matrix
T = np.eye(4)
for i in range(6):
    T_i = dh_transform(joint_angles[i], *dh_params[i][1:])
    T = np.dot(T, T_i)

# Extract the target coordinate point
target_point = T[:3, 3]
print("Target Coordinate Point:", target_point)
