from concurrent.futures import ThreadPoolExecutor
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cvzone
from back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as mymodel
from class_.Detection_face import FaceDetection
import cv2
import time
from back_end_process.Pyhton_files.class_.paths import paths1
import warnings
warnings.filterwarnings("ignore")

model = mymodel(paths1.images_path)
def myModel1(frame):
    threshold=0.8
    resoult = FaceDetection().face_detection(frame)

    for face, (x, y, w, h) in resoult:
        (final_naem, max_propablity) = model.face_recognition(face)
        if max_propablity < threshold:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cvzone.putTextRect(frame, " UNkoun ,Score : {}%".format(max_propablity), (x, y - 10),
                               scale=1, thickness=1)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            cvzone.putTextRect(frame, " {} IN ,Score : {}%".format(final_naem, round(max_propablity, 2) * 100),
                               (x, y - 10), scale=1, thickness=1)

        print("************************resoult************************ in ", final_naem)
    return frame
def process_frame(frame, func):
    return func(frame)

def main():
    cap = cv2.VideoCapture(0)
    # cap1 = cv2.VideoCapture(0)

    with ThreadPoolExecutor(max_workers=2) as executor:
        while cap.isOpened() and cap.isOpened():
            ret, frame = cap.read()
            height, width, _ = frame.shape

            # Define the rectangle to cover half of the camera view (left half)
            top_left_x = 0
            top_left_y = 0
            bottom_right_x = width // 2  # Half the width
            bottom_right_y = height

            # Draw the rectangle
            color = (0, 255, 0)  # Green color
            thickness = 2  # Thickness of the rectangle
            cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, thickness)

            # ret1, frame1 = cap.read()
            # if not ret or not ret1:
            #     print("Failed to grab frame")
            #     continue
            #
            # if frame1 is None or frame1.size == 0:
            #     print("Empty image, skipping cvtColor")
            #     continue  # Skip the processing for this frame

            future1 = executor.submit(process_frame, frame, myModel1)
            # future2 = executor.submit(process_frame, frame1, myModel1)

            cam1 = future1.result()
            # cam2 = future2.result()

            cv2.imshow("Image", cam1)

            if cv2.waitKey(1) & 0xFF == ord("t"):
                cap.release()
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                break

def take_sample_image_to_all_vedious():
    for vedio in os.listdir(r"..\vedious"):
        FaceDetection().take_a_sample_from_vidio(os.path.join(r"..\vedious", vedio))


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

# if __name__ == "__main__":
#
#     # take_sample_image_to_all_vedious()
#     # model.embading_all_images_Using_face_net_to_all_images()
#     # model.classfication_images_using_SVM()
#     main()
#     # record_vedio()










