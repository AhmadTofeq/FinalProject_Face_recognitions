import cv2
import os
import time
from cvzone.FaceDetectionModule import FaceDetector
from flask import current_app

def process_video(video, email):
    # Create directory for the staff member
    image_dir = os.path.join(current_app.root_path, 'videos', email)
    os.makedirs(image_dir, exist_ok=True)

    # Save the uploaded video temporarily
    temp_video_path = os.path.join(image_dir, "temp_video.mp4")
    video.save(temp_video_path)

    cap = cv2.VideoCapture(temp_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {temp_video_path}")
        return

    detector = FaceDetector(minDetectionCon=0.3, modelSelection=1)
    frame_count = 0
    saved_images_count = 0

    # Time tracking for saving images every 0.5 seconds
    last_save_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        faces, bboxes = detector.findFaces(frame, draw=False)
        current_time = time.time()

        if len(faces) > 0 and (current_time - last_save_time >= 0.5):
            for bbox in bboxes:
                x, y, w, h = bbox['bbox']
                # Ensure the bounding box is within the image bounds
                x = max(0, x)
                y = max(0, y)
                w = min(w, frame.shape[1] - x)
                h = min(h, frame.shape[0] - y)

                face_img = frame[y:y+h, x:x+w]

                if face_img.size == 0:
                    print("Warning: Detected face image is empty, skipping...")
                    continue

                face_filename = f"{email}_{frame_count}.jpg"
                face_path = os.path.join(image_dir, face_filename)
                cv2.imwrite(face_path, face_img)
                print(f"Saved: {face_path}")

                frame_count += 1
                saved_images_count += 1

            last_save_time = current_time

        # Stop if more than 3 images are saved
        if saved_images_count > 3:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Remove the temporary video file
    os.remove(temp_video_path)
