from concurrent.futures import ThreadPoolExecutor
import os
import json
from datetime import datetime
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cvzone
from back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as mymodel
#from class_.Detection_face import FaceDetection
import cv2
import time
from back_end_process.Pyhton_files.class_.paths import paths1
from flask import Response
import numpy as np 
def take_sample_image_to_all_vedious():
    for vedio in os.listdir(r"..\vedious"):

        FaceDetection().take_a_sample_from_vidio(os.path.join(r"..\vedious", vedio),vedio,45)







def record_vedio():
    # Ask for the video file name and path
    video_name = input("Enter the name of the video file (without extension): ") + ".mp4"
    save_path = r"F:\final_project\FinalProject_Face_recognitions\vedious"

    # Ensure the directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Complete file path
    file_path = os.path.join(save_path, video_name)

    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set camera properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = 30  # Set a higher frame rate for smoother video

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Using 'mp4v' for MP4 format
    out = cv2.VideoWriter(file_path, fourcc, frame_rate, (frame_width, frame_height))

    print("Recording video for 50 seconds...")

    start_time = time.time()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Write the frame into the file
            out.write(frame)

            # Display the resulting frame
            cv2.imshow('Recording', frame)

            # Check if 50 seconds have passed
            if time.time() - start_time > 50:
                break

            # Break the loop on 'q' key press to stop recording manually
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Failed to capture frame.")
            break

    # Release everything when the job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


class start_Presntation:
    def __init__(self,foile_name):
        self.path = os.path.join(paths1.json_files_path,
                            (foile_name+".json"))
        self.stafs=self.load_json(self.path)
        self.model = mymodel(paths1.images_path)


    def load_json(self,file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []
        return data

    def save_json(self, file_path):
        # Save the data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(self.stafs, file, indent=4)

    def create_entry(self,id_, name, date_time, case1):
        entry = {
            "id": id_,
            "name": name,
            "dateTime": str(date_time),
            "case": case1
        }
        self.stafs.append(entry)

    def save_to_json(self,id_, name, date_time, case1, filename='presentations.json'):
        # Save the updated data back to the JSON file
        with open(self.path, 'w') as file:
            json.dump(self.stafs, file, indent=4)
    def model_detection_and_recognition(self, frame, id_resntation,case):
        threshold = 0.8
        resoult = FaceDetection().face_detection(frame)
        for face, (x, y, w, h) in resoult:
            (final_naem, max_propablity) = self.model.face_recognition(face)
            if max_propablity < threshold:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
                cvzone.putTextRect(frame, " UNkoun ,Score : {}%".format(max_propablity), (x, y - 10),
                                   scale=1, thickness=1)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                id, name = (final_naem.split("@")[0], final_naem.split("@")[1])
                self.create_entry(id, name, date_time=datetime.now(), case1=case )
                cvzone.putTextRect(frame, " {} IN ,Score : {}%".format(final_naem, round(max_propablity, 2) * 100),
                                   (x, y - 10), scale=1, thickness=1)

            print("************************resoult************************ in ", final_naem)

        return frame

    def test_camera(self):
        cap = cv2.VideoCapture(0)
        cap1 = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            ret1, frame1 = cap.read()
            combined_frame = np.hstack((frame, frame1))
            cv2.imshow("Test Camera", combined_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Esc key
                break
            if cv2.getWindowProperty('Test Camera', cv2.WND_PROP_VISIBLE) < 1:
                break
        cap.release()
        cv2.destroyAllWindows()

    def main(self,id_presntation=15):
        cap = cv2.VideoCapture(0)
        # cap1 = cv2.VideoCapture(0)

        # with ThreadPoolExecutor(max_workers=1) as executor:
        while cap.isOpened() and cap.isOpened():
            ret, frame = cap.read()
            height, width, _ = frame.shape

            # # Define the rectangle to cover half of the camera view (left half)
            # top_left_x = 0
            # top_left_y = 0
            # bottom_right_x = width // 2  # Half the width
            # bottom_right_y = height

            # Draw the rectangle
            # color = (0, 255, 0)  # Green color
            # thickness = 2  # Thickness of the rectangle
            # cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, thickness)

            # ret1, frame1 = cap.read()
            # if not ret or not ret1:
            #     print("Failed to grab frame")
            #     continue
            #
            # if frame1 is None or frame1.size == 0:
            #     print("Empty image, skipping cvtColor")
            #     continue  # Skip the processing for this frame

            # future1 = executor.submit(process_frame, frame, myModel1)
            # future2 = executor.submit(process_frame, frame1, myModel1)

            # cam1 = future1.result()
            # cam2 = future2.result()
            cam1 = self.model_detection_and_recognition(frame, id_presntation,"IN")
            self.save_json(self.path)
            cv2.imshow("Presntation Start", cam1)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Esc key
                break
            if cv2.getWindowProperty('Presntation Start', cv2.WND_PROP_VISIBLE) < 1:
                break
        cap.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":

    # take_sample_image_to_all_vedious()
    # model.embading_all_images_Using_face_net_to_all_images()
    # model.classfication_images_using_SVM()
     start_Presntation("414").main(15)
    # record_vedio()
    #  test_camera()

def second_test_camera():
    def gen_frames():  
        cameras = []
        for i in range(5):  # Attempt to open up to 5 cameras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append((cap, i))  # Store the camera and its index

        if not cameras:
            return "Error: No cameras accessible"

        while True:
            frames = []
            for cap, index in cameras:
                success, frame = cap.read()
                if success:
                    # Put the camera index text on the frame
                    cv2.putText(frame, f'Camera {index + 1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    frames.append(frame)

            if frames:
                # Combine frames horizontally
                combined_frame = np.hstack(frames)
                ret, buffer = cv2.imencode('.jpg', combined_frame)
                frame = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break  # No frames to show, so break the loop

        for cap, _ in cameras:
            cap.release()

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')