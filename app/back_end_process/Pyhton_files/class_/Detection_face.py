import struct
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from cvzone.FaceDetectionModule import FaceDetector
from mtcnn.mtcnn import MTCNN
import cv2
import os
import time
from app.back_end_process.Pyhton_files.class_.paths import paths1
class FaceDetection:
    def __init__(self):
        self.detetion_model = FaceDetector(minDetectionCon=0.75, modelSelection=1)
        self.path_images = paths1.images_path
    def face_detection(self,frame):
        ####################################variables
        floating_point = 5
        accept_fake_and_real = True
        #############################################
        if not os.path.exists( self.path_images):
            os.makedirs( self.path_images)
        img, bboxs = self.detetion_model.findFaces(frame, draw=False)
        all_facees=[]
        if bboxs:
            for bbox in bboxs:
                # ---- Get Data  ---- #
                center = bbox["center"]
                x, y, w, h = bbox['bbox']
                score = int(bbox['score'][0] * 100)
                # ----------------------------------create my own custom rectange and drw it -----------------------------------
                # it used to change size rectangle and create a custom rectangle
                # x -= int(w * 0.2)
                # w += int((w * 0.2) * 1.5)
                # y -= int((h * 0.5))
                # h += int((h * 0.5) * 1.3)

                # ------------------------------------ to avoidind value of x,y,w.h  is not gonna be below zero for that we have to --------------------------------
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                # ----------------------------------- find picture bluriness -----------------------------------------------

                image_face = img[y:y + h, x:x + w]
                image_face= cv2.resize(image_face,(160,160))
                all_facees.append([image_face, (x, y, w, h)])

        return all_facees
    def embadaing_image(self,data):
        # load the image
        detector =MTCNN()
        # detect faces in the image
        faces = detector.detect_faces(data)
        resuly=[]
        for face in faces:
            # get coordinates
            x, y, w, h = face['box']
            image_face=data[y:y + h, x:x + w]
            resuly.append([image_face, (x, y, w, h)])

        return resuly
    def take_a_sample_from_vidio(self, video_path,name,id):
        ####################################variables
        img_counter = 0
        id=str(id)
        video_name = id+"@"+name
        save_folder = os.path.join(self.path_images, video_name)  # Folder to save the detected faces
        clarity_threshold = 10.0  # Set your clarity threshold here
        #############################################
        # Create the save folder if it does not exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Initialize the video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        # Initialize the FaceDetector object
        # Track time for saving images every 0.5 seconds
        last_save_time = time.time()
        # Run the loop to continually get frames from the video
        while True:
            # Read the current frame from the video
            success, img = cap.read()
            if not success:
                break

            # Detect faces in the image
            resoult  = self.face_detection(img)

            # Check if any face is detected
            if resoult:
                current_time = time.time()
                if current_time - last_save_time >= 0.5:
                    for face,(x, y, w, h) in resoult:
                        img_name = os.path.join(save_folder, f"{id + '@' + name}.{img_counter}.png")
                        cv2.imwrite(img_name, face)
                        img_counter += 1
                    last_save_time = current_time

        cap.release()
        print("Processing complete. Images saved in the '{}' folder.".format(save_folder))
        return save_folder
#
# if __name__ == "__main__":
#     face_detection = FaceDetection()
#     face_detection.take_a_sample_from_vidio(r"F:\final_project\Ui\FinalProject_Face_recognitions\vedious\m_sami.mp4","zasd","soran232@cs.dr")