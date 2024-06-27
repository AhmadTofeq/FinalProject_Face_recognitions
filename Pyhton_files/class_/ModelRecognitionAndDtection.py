
import cv2 as cv2
import os
import time

class ModelRecognitionAndDtection1:
    def __init__(self,_recognition_moddel,_detetion_model,_desiosion_model,_path_data_images):
        self.recognition_moddel=_recognition_moddel
        self.detetion_model = _detetion_model
        self.desiosion_model = _desiosion_model
        self.path_data_images = _path_data_images
    def face_detection(self,frame):
        pass
    def face_recognition(self,image):
        pass
    def split_date_test_and_train(self):
        pass
    def take_a_sample_from_vidio(self, video_path):

        ####################################variables
        floating_point = 5
        img_counter = 0
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        save_folder =os.path.join(self.path_data_images,video_name)  # Folder to save the detected faces
        clarity_threshold = 100.0  # Set your clarity threshold here
        #############################################
        print("*************************************************",save_folder)
        # Create the save folder if it does not exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Initialize the video capture
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        # Initialize the FaceDetector object
        detector = self.detetion_model(minDetectionCon=0.3, modelSelection=1)

        # Track time for saving images every 0.5 seconds
        last_save_time = time.time()
        # Run the loop to continually get frames from the video
        while True:
            # Read the current frame from the video
            success, img = cap.read()
            if not success:
                break

            # Detect faces in the image
            img, bboxs = detector.findFaces(img, draw=False)

            # Check if any face is detected
            if bboxs:
                current_time = time.time()
                if current_time - last_save_time >= 0.5:
                    for bbox in bboxs:
                        # Get bounding box coordinates
                        x, y, w, h = bbox['bbox']

                        # Adjust bounding box size
                        x -= int(w * 0.2)
                        w += int((w * 0.2) * 1.5)
                        y -= int((h * 0.5))
                        h += int((h * 0.5) * 1.3)

                        # Ensure the bounding box is within the image bounds
                        x = max(0, x)
                        y = max(0, y)
                        w = max(0, w)
                        h = max(0, h)

                        # Extract the face region from the image
                        image_face = img[y:y + h, x:x + w]

                        # Calculate the clarity of the face image
                        gray_face = cv2.cvtColor(image_face, cv2.COLOR_BGR2GRAY)
                        variance_of_laplacian = cv2.Laplacian(gray_face, cv2.CV_64F).var()

                        # Save the detected face image only if it meets the clarity threshold
                        if variance_of_laplacian >= clarity_threshold:
                            img_name =os.path.join(save_folder,f"{video_name}_{img_counter}.png")
                            image_face=cv2.resize(image_face,(160,160))
                            cv2.imwrite(img_name, image_face)
                            img_counter += 1
                    last_save_time = current_time

        cap.release()
        print("Processing complete. Images saved in the '{}' folder.".format(save_folder))

