from sklearn.svm import SVC as classifier_SVM
from sklearn.model_selection import GridSearchCV
import numpy as np
import pickle
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
import cv2
import os
from back_end_process.Pyhton_files.class_.paths import paths1
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
class ModelRecognitionAndDtection1:
    def __init__(self,_path_data_images):
        self.embedding_image=FaceNet()
        self.SVM_disesion = pickle.load(open(paths1.SVM_model, 'rb'))
        self.path_data_images = _path_data_images
        self.emmbeading_model = np.load(paths1.embading_model)
        y = self.emmbeading_model['arr_1']
        self.encoder = LabelEncoder().fit(y)

    def get_embedding(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_img = img.astype('float32')
        face_img = np.expand_dims(img, axis=0)
        return self.embedding_image.embeddings(face_img)[0]
    def face_recognition(self,face):
        ypred=self.get_embedding(face)
        # ypred=self.rediuce_dimentiin(ypred1)
        ypred_popabilty = self.SVM_disesion.predict_proba([ypred])
        max_propabilty=max(ypred_popabilty[0])
        index_max_propabilty=np.where(ypred_popabilty[0]==max_propabilty)[0]
        convert_Number_to_real_name = self.encoder.inverse_transform(index_max_propabilty)
        return (convert_Number_to_real_name,max_propabilty)

    # def rediuce_dimentiin(self,embading_face):
    #     x = tf.reshape(embading_face, [1, 512, 1])
    #     avg_pool_1d = tf.keras.layers.AveragePooling1D(pool_size=2, strides=2, padding='valid')
    #     x = avg_pool_1d(x)
    #     x = np.squeeze(x)
    #     return x


    def split_date_test_and_train(self):
        pass

    def embading_all_images_Using_face_net_to_one_persone(self):
        x_image = []
        y_lable = []
        print(self.emmbeading_model["arr_0"].shape)
        print(self.emmbeading_model["arr_1"].shape)
        for folders_image in os.listdir(self.path_data_images):
            x_image.append(self.get_embedding(
                cv2.imread(os.path.join(self.path_data_images,folders_image))))
            y_lable.append(os.path.basename(self.path_data_images))

        image_future=self.emmbeading_model['arr_0']
        lable=self.emmbeading_model['arr_1']
        y_lable=lable.tolist()+y_lable
        x_image=image_future.tolist()+x_image
        np.savez_compressed(paths1.embading_model, x_image, y_lable)
        print("done................................................")

    def embading_all_images_Using_face_net_to_all_images(self):
        x_image = []
        y_lable = []
        for folders_image in os.listdir(self.path_data_images):
            for image in os.listdir(os.path.join(self.path_data_images,folders_image)):
                x_image.append(self.get_embedding(
                    cv2.imread(os.path.join(self.path_data_images,folders_image,image))))
                y_lable.append(folders_image)
        np.savez_compressed(paths1.embading_model, x_image, y_lable)

    def classfication_images_using_SVM(self):
        print(self.emmbeading_model['arr_0'].shape)
        print(self.emmbeading_model['arr_1'])
        embedding_images=self.emmbeading_model['arr_0']
        encoder = LabelEncoder()
        encoder.fit(self.emmbeading_model['arr_1'])
        lables = encoder.transform(self.emmbeading_model['arr_1'])
        svm = classifier_SVM(kernel='rbf', probability=True)
        # Define the parameter grid for C and gamma
        param_grid = {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['rbf','linear']
        }
        # Use GridSearchCV to find the best parameters
        grid_search = GridSearchCV(svm, param_grid, cv=4, scoring='accuracy')
        grid_search.fit(embedding_images, lables)
        # Get the best model
        print("########################beast paramiter's for SVM ",grid_search.best_params_)
        print("########################beast Score ",grid_search.best_score_)

        # y_pred = best_model.predict(embedding_images)
        # print("Predect_ tast data :", y_pred)
        # print("actual_  tast data :", y_lable_encode)

        with open(paths1.SVM_model, 'wb') as f:
            pickle.dump(grid_search.best_estimator_, f)
# if __name__=="__main__":
#     mod =ModelRecognitionAndDtection1(r"F:\final_project\Ui\FinalProject_Face_recognitions\Colect_Data\all_images\ahmad1212@testttttt")
#     mod.embading_all_images_Using_face_net_to_one_persone()