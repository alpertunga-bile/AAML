import cv2
import os
from tqdm import tqdm

video_list = [video for video in os.listdir() if video.endswith('.mp4')]

for video in video_list:
    video_name = video.split('.')[0]
    if os.path.exists(video_name):
        continue
    else:
        os.mkdir(video_name)
    video_path = video_name + '/'
    video_cap = cv2.VideoCapture(video)
    total_frame = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(video_cap.get(cv2.CAP_PROP_FPS))
    frame_lock = frame_rate * 3
    for i in tqdm(range(0, total_frame), desc=f"{video_name}"):
        success, image = video_cap.read()
        if i % frame_lock == 0:
            cv2.imwrite(f"{video_path}{video_name}_{i}.png", image)
    video_cap.release()
