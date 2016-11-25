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

# Calulate angle between to row vectors
def calculate_angle2D(u,v):
    v = normalize(v)
    u = normalize(u)
    return float(np.arccos(np.transpose(u) @ v))

# Calulate directed angle from u to v, counter clockwise
def directed_angle2D(u,v):
    u = normalize(u)
    v = normalize(v)
    angle = math.atan2(v[1], v[0]) - math.atan2(u[1], u[0])
    if angle%np.pi == 0:
        return abs(angle)%(2*np.pi)*np.sign(angle)
    else:
        return abs(angle)%np.pi*np.sign(angle)

# checks if other agent is neighbour to agent
def is_neighbour(agent, other_agent, radius2, field_of_view = -1):
    if agent == other_agent:
        return (False, agent.position)

    for i in range(9):
        u = other_agent.positions[i] - agent.position;
        distance2 = (u[0]**2 + u[1]**2)
        
        if distance2 <= radius2:
            if field_of_view == -1: #No limitation on field of view
                return (True, other_agent.positions[i])
            else:                
                angle = calculate_angle2D(agent.velocity, other_agent.position)
                if angle <= field_of_view:
                    return True
    return (False, agent.position)

def rotate_ccw(u,theta): #rotate vector counter clockwise
    shape = u.shape
    u = np.reshape(u,[2,1])
    R = [[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]]
    v =  R @ u
    return np.reshape(v,shape)
