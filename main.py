from utils import (read_video, save_video)
from trackers import PlayerTracker
from trackers import BallTracker
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
import cv2

def main():

    # Read Video
    input_video_path="input_video/input_video.mp4"
    input_frames=read_video(input_video_path)

    # Detect Players
    player_tracker=PlayerTracker('yolov8x')
    ball_tracker=BallTracker('weights/best.pt')
    court_line_detector=CourtLineDetector('weights/keypoints_model.pth')
    mini_court=MiniCourt(input_frames[0])
    # print(input_frames[0].shape)

    detected_keypoints=court_line_detector.predict_on_image(input_frames[0])

    player_detections=player_tracker.detect_frames(input_frames,read_from_stub=True,stub_path="trackers/tracker_stubs/player_detections.pkl")
    ball_detections=ball_tracker.detect_frames(input_frames,read_from_stub=True,stub_path="trackers/tracker_stubs/ball_detections.pkl")
    output_frames=player_tracker.draw_bboxes(input_frames,player_detections)
    output_frames=ball_tracker.draw_bboxes(output_frames,ball_detections)
    output_frames=court_line_detector.draw_keypoints_on_video(output_frames,detected_keypoints)
    output_frames=mini_court.draw_minicourt(output_frames)

    ball_hit_frames=ball_tracker.get_ball_hit_frame(ball_detections)
    print(ball_hit_frames)
     # Draw frame number on top left corner
    for i, frame in enumerate(output_frames):
        frame=cv2.putText(frame, f"Frame: {i}",(10,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    output_video_path="output_videos/output_video.mp4"

    save_video(output_frames,output_video_path)



if __name__ == "__main__":
    main()


