from  ultralytics import YOLO

# model=YOLO(r'weights\best.pt')
model=YOLO(r'yolov8x')
model.track('./input_video/input_video.mp4',conf=0.2,save=True)






