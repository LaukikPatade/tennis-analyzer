import cv2
import numpy as np
import sys
# sys.path.append('../')
# from constants import DOUBLE_LINE_WIDTH, HALF_COURT_LINE_HEIGHT, DOUBLE_ALLY_DIFFERENCE, NO_MANS_LAND_HEIGHT, SINGLE_LINE_WIDTH



from utils import convert_pixel_to_actual,convert_actual_to_pixel,get_center,measure_distance,get_foot_position

constants={
    "SINGLE_LINE_WIDTH" : 8.23,
"DOUBLE_LINE_WIDTH" : 10.97,
"HALF_COURT_LINE_HEIGHT" : 11.88,
"SERVICE_LINE_WIDTH" : 6.4,
"DOUBLE_ALLY_DIFFERENCE" : 1.37,
"NO_MANS_LAND_HEIGHT" : 5.48,
"PLAYER_1_HEIGHT_METERS" : 1.88,
"PLAYER_2_HEIGHT_METERS" : 1.91
}

class MiniCourt():
    def __init__(self,frame):
        self.drawing_rectangle_width=250
        self.drawing_rectangle_height=500
        self.buffer=50
        self.padding_court=20
        self.court_lines=[
            (0,1),
            (1,3),
            (3,2),
            (2,0),
            (0,1),
            (4,5),
            (7,6),
            (8,9),
            (11,10),
            (12,13)
        ]

        self.set_canvas_bg_box_pos(frame)
        self.set_minicourt_pos()
        self.set_court_kps()
        # print(constants)
        # print(DOUBLE_LINE_WIDTH)
        # self.set_court_kps()

    
    def convert_act_2_pix_dist(self,act_dist):
        return convert_actual_to_pixel(act_dist,constants['DOUBLE_LINE_WIDTH'],self.court_drawing_width)

    def set_court_kps(self):
        drawing_key_points = [0]*28

        # point 0 
        drawing_key_points[0] , drawing_key_points[1] = int(self.court_start_x), int(self.court_start_y)
        # point 1
        drawing_key_points[2] , drawing_key_points[3] = int(self.court_end_x), int(self.court_start_y)
        # point 2
        drawing_key_points[4] = int(self.court_start_x)
        drawing_key_points[5] = self.court_start_y + self.convert_act_2_pix_dist(constants['HALF_COURT_LINE_HEIGHT']*2)
        # point 3
        drawing_key_points[6] = drawing_key_points[0] + self.court_drawing_width
        drawing_key_points[7] = drawing_key_points[5] 
        # #point 4
        drawing_key_points[8] = drawing_key_points[0] +  self.convert_act_2_pix_dist(constants['DOUBLE_ALLY_DIFFERENCE'])
        drawing_key_points[9] = drawing_key_points[1] 
        # #point 5
        drawing_key_points[10] = drawing_key_points[4] + self.convert_act_2_pix_dist(constants['DOUBLE_ALLY_DIFFERENCE'])
        drawing_key_points[11] = drawing_key_points[5] 
        # #point 6
        drawing_key_points[12] = drawing_key_points[2] - self.convert_act_2_pix_dist(constants['DOUBLE_ALLY_DIFFERENCE'])
        drawing_key_points[13] = drawing_key_points[3] 
        # #point 7
        drawing_key_points[14] = drawing_key_points[6] - self.convert_act_2_pix_dist(constants['DOUBLE_ALLY_DIFFERENCE'])
        drawing_key_points[15] = drawing_key_points[7] 
        # #point 8
        drawing_key_points[16] = drawing_key_points[8] 
        drawing_key_points[17] = drawing_key_points[9] + self.convert_act_2_pix_dist(constants['NO_MANS_LAND_HEIGHT'])
        # # #point 9
        drawing_key_points[18] = drawing_key_points[16] + self.convert_act_2_pix_dist(constants['SINGLE_LINE_WIDTH'])
        drawing_key_points[19] = drawing_key_points[17] 
        # #point 10
        drawing_key_points[20] = drawing_key_points[10] 
        drawing_key_points[21] = drawing_key_points[11] - self.convert_act_2_pix_dist(constants['NO_MANS_LAND_HEIGHT'])
        # # #point 11
        drawing_key_points[22] = drawing_key_points[20] +  self.convert_act_2_pix_dist(constants['SINGLE_LINE_WIDTH'])
        drawing_key_points[23] = drawing_key_points[21] 
        # # #point 12
        drawing_key_points[24] = int((drawing_key_points[16] + drawing_key_points[18])/2)
        drawing_key_points[25] = drawing_key_points[17] 
        # # #point 13
        drawing_key_points[26] = int((drawing_key_points[20] + drawing_key_points[22])/2)
        drawing_key_points[27] = drawing_key_points[21] 

        self.drawing_key_points=drawing_key_points

        
    def set_minicourt_pos(self):
        self.court_start_x=self.start_x+self.padding_court
        self.court_end_x=self.end_x-self.padding_court
        self.court_start_y=self.start_y+self.padding_court
        self.court_end_y=self.end_y-self.padding_court
        self.court_drawing_width=self.court_end_x-self.court_start_x

    
    def set_canvas_bg_box_pos(self,frame):
        self.end_x=frame.shape[1]-self.buffer
        self.start_x=self.end_x-self.drawing_rectangle_width
        self.end_y=self.buffer+self.drawing_rectangle_height
        self.start_y=self.buffer

    
    def draw_bg_rect(self,frame):
        shapes=np.zeros_like(frame,np.uint8)

        cv2.rectangle(shapes,(self.start_x,self.start_y),(self.end_x,self.end_y),(255,255,255),-1)

        out=frame.copy()
        alpha=0.5
        mask=shapes.astype(bool)
        out[mask]=cv2.addWeighted(frame,alpha,shapes,1-alpha,0)[mask]
        # out=cv2.cvtColor(out,cv2.COLOR_BGR2RGB)

        return out
    
    def draw_court_structure(self,frame):
        out=frame.copy()
        for i in range(len(self.drawing_key_points)):
            if(i%2==0):
                cv2.circle(out,(int(self.drawing_key_points[i]),int(self.drawing_key_points[i+1])),5,(0,0,255),-1)

         # draw Lines
        for line in self.court_lines:
            start_point = (int(self.drawing_key_points[line[0]*2]), int(self.drawing_key_points[line[0]*2+1]))
            end_point = (int(self.drawing_key_points[line[1]*2]), int(self.drawing_key_points[line[1]*2+1]))
            cv2.line(out, start_point, end_point, (0, 0, 0), 2)

        # Draw net
        net_start_point = (self.drawing_key_points[0], int((self.drawing_key_points[1] + self.drawing_key_points[5])/2))
        net_end_point = (self.drawing_key_points[2], int((self.drawing_key_points[1] + self.drawing_key_points[5])/2))
        cv2.line(out, net_start_point, net_end_point, (255, 0, 0), 2)

        return out   

    def draw_minicourt(self,frames):
        output_frames=[]
        for frame in frames:
            frame=self.draw_bg_rect(frame)
            frame=self.draw_court_structure(frame)
            output_frames.append(frame)

        return output_frames
    
    def draw_court_lines(self,frame):
        out=frame.copy()
        for line in self.court_lines:
            out=cv2.line(out,(int(self.drawing_key_points[line[0]]),int(self.drawing_key_points[line[0]+1])),(int(self.drawing_key_points[line[1]]),int(self.drawing_key_points[line[1]+1])),(0,0,255),2)

        return out
    
    def convert_bb_box_to_minicourt_coordinates(self,player_boxes,ball_boxes,court_kps):
        player_heights={
            1:constants['PLAYER_1_HEIGHT_METERS'],
            2:constants['PLAYER_2_HEIGHT_METERS']
        }


        output_player_boxes=[]
        output_ball_boxes=[]

        for frame_num,player_bbox in enumerate(player_boxes):
            for player_id,bbox in player_bbox.items():
                foot_position=get_foot_position(bbox)

                # get closest keypoint in pixels
                closest_kps=get_closest_keypoint(foot_position,court_kps,[0,2,12,13])

                
                



        
            

        