import numpy as np
import math

# converts a direction vector to angle in clockwise rotation from (1,0)
def dir_to_angle(dir):
     #angle = mod(atan2(x1*y2-x2*y1,x1*x2+y1*y2),2*pi);
     x1 = 1
     y1 = 0
     x2 = dir[0]
     y2 = dir[1]
     angle = math.atan2(x1*y2-x2*y1,x1*x2+y1*y2)
     return -(angle * 180 / math.pi)

# returns normalized vector
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return np.array([1,0])
    return v/norm
