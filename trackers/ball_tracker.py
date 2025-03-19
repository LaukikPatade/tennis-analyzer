from ultralytics import YOLO
import cv2
import numpy as np
import pickle
import pandas as pd


class BallTracker:
    def __init__(self,model_path):
        self.model=YOLO(model_path)

    def detect_frames(self,frames,read_from_stub=False,stub_path=None):
        ball_detections=[]

        if read_from_stub and stub_path is not None:
            with open(stub_path,'rb') as f:
                ball_detections=pickle.load(f)        
        else:
            for frame in frames:
                ball_dict=self.detect_frame(frame)
                ball_detections.append(ball_dict)
            with open(stub_path,'wb') as f:
                pickle.dump(ball_detections,f)

        ball_detections=self.interpolate_ball_detections(ball_detections)
        return ball_detections
    
    def detect_frame(self,input_frame):
        results= self.model.predict(input_frame,conf=0.15)[0]
        print(len(results.boxes))
        ball_dict={}


        for box in results.boxes:
            result=box.xyxy.tolist()[0]
            ball_dict[1]=result
        
        return ball_dict

    def interpolate_ball_detections(self,ball_detections):
        ball_detections=[x.get(1,[]) for x in ball_detections]
        df_bd=pd.DataFrame(ball_detections,columns=['x1','y1','x2','y2'])
        df_bd=df_bd.interpolate()
        df_bd=df_bd.bfill()
        ball_detections=[{1:x} for x in df_bd.to_numpy().tolist()]
        return ball_detections




    def draw_bboxes(self,video_frames,ball_detections):
        output_video_frames=[]
        for frame, ball_dict in zip(video_frames,ball_detections):
            # Draw Bounding Boxes
            for track_id,bbox in ball_dict.items():
                x1,y1,x2,y2=bbox
                cv2.putText(frame,f"Ball ID : {track_id}",(int(bbox[0]),int(bbox[1]-10)),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)
                cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),2)
            output_video_frames.append(frame)
        
        return output_video_frames
    
    def get_ball_hit_frame(self,ball_detections):
        ball_detections=[x.get(1,[]) for x in ball_detections]
        df_bd=pd.DataFrame(ball_detections,columns=['x1','y1','x2','y2'])
        df_bd['y']=(df_bd['y1']+df_bd['y2'])/2
        df_bd['delta_y']=df_bd['y'].diff()
        df_bd['ball_hit']=0
        for i in range(len(df_bd)):
            negative_position_change=df_bd['delta_y'].iloc[i]>0 and df_bd['delta_y'].iloc[i-1]<0
            positive_position_change=df_bd['delta_y'].iloc[i]<0 and df_bd['delta_y'].iloc[i-1]>0
            if negative_position_change or positive_position_change:
                df_bd.loc[i-1,'ball_hit']=1
        ball_hit_frames=df_bd[df_bd['ball_hit']==1].index.tolist()
        return ball_hit_frames
