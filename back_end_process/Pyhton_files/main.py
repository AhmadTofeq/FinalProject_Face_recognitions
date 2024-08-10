
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cvzone
from back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as mymodel
from class_.Detection_face import FaceDetection
import cv2
import time
from back_end_process.Pyhton_files.class_.paths import paths1
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
def main():
    # its to recognition
    cap = cv2.VideoCapture(0)
    # cap1 = cv2.VideoCapture(1)
    while cap.isOpened():
        ret, frame = cap.read()
        # ret1, frame1 = cap1.read()
        cam1=myModel1(frame)
        # cam2=myModel1(frame1)
        # cv2.imshow("Image", cv2.hconcat([cam1,cam2]))
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
#
# if __name__ == "__main__":
#
#     # take_sample_image_to_all_vedious()
#     # model.embading_all_images_Using_face_net_to_all_images()
#     # model.classfication_images_using_SVM()
#     main()
#     # record_vedio()










