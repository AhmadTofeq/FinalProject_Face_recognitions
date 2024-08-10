from back_end_process.Pyhton_files.class_.paths import paths1
import numpy as np
from back_end_process.Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1
import os
class model_trainning:
    def __init__(self):
        paths = paths1
        self.embeading_model=paths.embading_model
        self.SVM_clsaification=paths.SVM_model
        self.all_image_path=paths.images_path
    def clean_Facce_net_model(self):
        try:
            np.savez_compressed(self.embeading_model, [], [])
            return True
        except Exception as e:
            return False
        # ModelRecognitionAndDtection1(self.all_image_path).classfication_images_using_SVM()
    def model_trainin_Face_net(self):
        try:
            ModelRecognitionAndDtection1(self.all_image_path).embading_all_images_Using_face_net_to_all_images()
            return True
        except Exception as e:
            return False

    def model_classification(self):
        # you can directly use this line when you want used
        ModelRecognitionAndDtection1(self.all_image_path).classfication_images_using_SVM()

    def get_directory_images_by_id(self ,id_staff):
        id_staff=str(id_staff)
        for i in os.listdir(self.all_image_path):
            if i.split("@")[0] == id_staff:
                return os.path.join(self.all_image_path, i)
        else:
            return "Null"


# if __name__ == "__main__":
    # take_sample_image_to_all_vedious()
   # print( model_trainning().get_directory_images_by_id("2"))