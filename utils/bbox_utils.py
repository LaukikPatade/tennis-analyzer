def get_center(bbox):
    x1,y1,x2,y2=bbox
    center_x=(x1+x2)/2
    center_y=(y1+y2)/2
    return (int(center_x),int(center_y))

def measure_distance(p1,p2):
    return((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5
    
def get_foot_position(bbox):
    x1,y1,x2,y2=bbox
    return (int((x1+x2)/2),int(y2))

def get_closest_keypoint(foot_position,court_kps,keypoint_indices):
    min_distance=float('inf')
    closest_keypoint=None
    for index in keypoint_indices:
        keypoint=(keypoint[index*2],keypoint[index*2+1])
        if(keypoint.index in keypoint_indices):
            distance=measure_distance(foot_position,keypoint.position)
            if(distance<min_distance):
                min_distance=distance
                closest_keypoint=keypoint
    return closest_keypoint



