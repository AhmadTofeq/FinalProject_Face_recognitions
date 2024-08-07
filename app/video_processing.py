import cv2
import os
import time
import numpy as np
from flask import current_app
from app.back_end_process.Pyhton_files.class_.Detection_face import FaceDetection as mymodel
from app.back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as emmbeding
from app.back_end_process.Pyhton_files.class_.paths import paths1

class StaffProcessor:

    def __init__(self):
        pass

    def insert_staff(self, video_path, name, id):
        # Create directory for the staff member
        #     image_dir = os.path.join(r"F:\final_project\Ui\FinalProject_Face_recognitions", 'videos1', name)
        #     os.makedirs(image_dir, exist_ok=True)
        #
        #     # Save the uploaded video temporarily
        #     temp_video_path = os.path.join(image_dir, "temp_video.mp4")
        #     video_path.save(temp_video_path)
        model = mymodel().take_a_sample_from_vidio(video_path, name, id)
        emmbeding(model).embading_all_images_Using_face_net_to_one_persone()
        emmbeding(paths1.images_path).classfication_images_using_SVM()
        # Remove the temporary video file
        # os.remove(temp_video_path)

    def updated_staff(self, video, name, id):
        if video == "":
            # if you want just update name staff
            # step one update image where id is equal to this id
            id = str(id)
            video_name = id + "@" + name
            # if not os.path.exists(paths1.images_path):
            #    return
            for i in os.listdir(paths1.images_path):
                # print(i)
                if i.split("@")[0] == id:
                    for image in os.listdir(os.path.join(paths1.images_path, i)):
                        old_file_name = os.path.join(paths1.images_path, i, image)
                        new_file_name = os.path.join(paths1.images_path, i, (video_name + "." + image.split(".")[1] + ".png"))
                        os.rename(old_file_name, new_file_name)
                    else:
                        old_file_name = os.path.join(paths1.images_path, i)
                        new_file_name = os.path.join(paths1.images_path, i.split("@")[0] + "@" + name)
                        os.rename(old_file_name, new_file_name)

            # change label video in model embedding
            with np.load(paths1.embading_model, mmap_mode='r+') as data:
                arr_0 = data["arr_0"]
                arr_1 = data["arr_1"].copy()
            new_label = []
            for i, label in enumerate(arr_1):
                if label.split("@")[0] == id:
                    # print(label.split("@")[0] + "@" + name)
                    new_label.append(label.split("@")[0] + "@" + name)
                else:
                    new_label.append(label)
            np.savez_compressed(paths1.embading_model, arr_0, new_label)

            emmbeding(paths1.images_path).classfication_images_using_SVM()
            # update their label according to id
            pass
        else:
            for i in os.listdir(paths1.images_path):
                if i.split("@")[0] == id:
                    os.remove(os.path.join(paths1.images_path, i))
            with np.load(paths1.embading_model, mmap_mode='r+') as data:
                arr_0 = data["arr_0"]
                arr_1 = data["arr_1"].copy()
                new_x = []
                new_label = []
            for i, label in enumerate(arr_1):
                if label.split("@")[0] != id:
                    new_x.append(arr_0[i])
                    new_label.append(arr_1[i])

            np.savez_compressed(paths1.embading_model, new_x, new_label)
            # Create directory for the staff member
            # --now start to add new video
            self.insert_staff(video, name, id)
