import os
import numpy as np
from back_end_process.Pyhton_files.class_.Detection_face import FaceDetection as mymodel
from back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as emmbeding
from back_end_process.Pyhton_files.class_.paths import paths1
import shutil
class StaffProcessor:

    def __init__(self):
        pass

    def insert_staff(self, video_path, name, id_staff):
        model = mymodel().take_a_sample_from_vidio(video_path, name, id_staff)
        emmbeding(model).embading_all_images_Using_face_net_to_one_persone()
        emmbeding(paths1.images_path).classfication_images_using_SVM()

    def updated_staff(self, video, name, id_staff):
        print("******************************************************")
        id_staff = str(id_staff)
        video_name = id_staff + "@" + name
        print(video)
        if not paths1.images_path:
            raise ValueError("The images path is not set.")
        
        if video == "":
            # Handle case when no new video is provided
            for i in os.listdir(paths1.images_path):
                if i.split("@")[0] == id_staff:
                    temp_dir = os.path.join(paths1.images_path, 'temp_' + i)
                    os.makedirs(temp_dir, exist_ok=True)
                    for image in os.listdir(os.path.join(paths1.images_path, i)):
                        old_file_name = os.path.join(paths1.images_path, i, image)
                        new_file_name = os.path.join(temp_dir, (video_name + "." + image.split(".")[1] + ".png"))
                        
                        # Validate file paths
                        if not old_file_name or not new_file_name:
                            raise ValueError("One of the file paths is not set.")
                        
                        # Debugging statements
                        print(f"Renaming {old_file_name} to {new_file_name}")
                        
                        os.rename(old_file_name, new_file_name)
                    shutil.rmtree(os.path.join(paths1.images_path, i))
                    os.rename(temp_dir, os.path.join(paths1.images_path, video_name))

            with np.load(paths1.embading_model, mmap_mode='r+') as data:
                arr_0 = data["arr_0"]
                arr_1 = data["arr_1"].copy()
            new_label = []
            for i, label in enumerate(arr_1):
                if label.split("@")[0] == id_staff:
                    new_label.append(label.split("@")[0] + "@" + name)
                else:
                    new_label.append(label)
            np.savez_compressed(paths1.embading_model, arr_0, new_label)

            emmbeding(paths1.images_path).classfication_images_using_SVM()
        else:
            # Handle case when a new video is provided
            is_have_a_vedio=False
            for i in os.listdir(paths1.images_path):
                if i.split("@")[0] == id_staff:
                    is_have_a_vedio = True
                    shutil.rmtree(os.path.join(paths1.images_path, i))
            if not is_have_a_vedio:
                self.insert_staff(video, name, id_staff)
                return
            with np.load(paths1.embading_model, mmap_mode='r+') as data:
                arr_0 = data["arr_0"]
                arr_1 = data["arr_1"].copy()
                new_x = []
                new_label = []
            for i, label in enumerate(arr_1):
                if label.split("@")[0] != id_staff:
                    new_x.append(arr_0[i])
                    new_label.append(arr_1[i])

            np.savez_compressed(paths1.embading_model, new_x, new_label)
            self.insert_staff(video, name, id_staff)

    def delete_images_and_labels(self, staff_id):
        staff_id = str(staff_id)

        # Delete images
        for i in os.listdir(paths1.images_path):
            if i.split("@")[0] == staff_id:
                shutil.rmtree(os.path.join(paths1.images_path, i))
                break

        # Remove labels from the embedding model
        with np.load(paths1.embading_model, mmap_mode='r+') as data:
            arr_0 = data["arr_0"]
            arr_1 = data["arr_1"].copy()
            new_x = []
            new_label = []
            for i, label in enumerate(arr_1):
                if label.split("@")[0] != staff_id:
                    new_x.append(arr_0[i])
                    new_label.append(arr_1[i])

        np.savez_compressed(paths1.embading_model, new_x, new_label)
        emmbeding(paths1.images_path).classfication_images_using_SVM()