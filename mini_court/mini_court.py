import cv2
import constants
from utils import convert_pixel_to_actual,convert_actual_to_pixel

class MiniCourt():
    def __init__(self,frame):
        self.drawing_rectangle_width=250
        self.drawing_rectangle_height=450
        self.buffer=50
        self.padding_court=20

        self.set_canvas_bg_box_pos(frame)
        self.set_minicourt_pos()
    
    def convert_act_2_pix_dist(self,act_dist):
        return convert_actual_to_pixel(constants.HALF_COURT_LINE_HEIGHT*2,constants.DOUBLE_LINE_WIDTH,self.court_drawing_width)

    def set_court_kps(self):
        drawing_kps=[0]*28
         
        # point 0
        drawing_kps[0],drawing_kps[1]=int(self.court_start_x), int(self.court_start_y)

        # point 1
        drawing_kps[2],drawing_kps[3]=int(self.court_end_x),  drawing_kps[1]

        # point 2
        drawing_kps[4],drawing_kps[5]= drawing_kps[0], drawing_kps[1]+self.convert_act_2_pix_dist(constants.HALF_COURT_LINE_HEIGHT*2)

        # point 3
        drawing_kps[6],drawing_kps[7]=drawing_kps[0]+self.court_drawing_width,drawing_kps[5]

        # point 4
        drawing_kps[0],drawing_kps[1]=drawing_kps[0]+self.convert_act_2_pix_dist(constants.DOUBLE_ALLEY_DIFFERENCE), drawing_kps[1]

        
        



    def set_minicourt_pos(self):
        self.court_start_x=self.start_x+self.padding_court
        self.court_end_x=self.end_x-self.padding_court
        self.court_start_y=self.start_y+self.padding_court
        self.court_end_y=self.end_y-self.padding_court
        self.court_drawing_width=self.court_end_x-self.court_start_x

    
    def set_canvas_bg_box_pos(self,frame):
        frame=frame.copy

        self.end_x=frame.shape[1]-self.buffer
        self.start_x=self.end_x-self.drawing_rectangle_width
        self.end_y=self.buffer+self.drawing_rectangle_height
        self.start_y=self.buffer


        