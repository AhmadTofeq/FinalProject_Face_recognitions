from sklearn.model_selection import train_test_split
import cvzone
from sklearn.preprocessing import LabelEncoder
from Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as mymodel
from cvzone.FaceDetectionModule import FaceDetector
from keras_facenet import FaceNet
import pickle
import cv2
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
path_images= r"..\Colect_Data\all_images"
model = mymodel("", FaceDetector(minDetectionCon=0.3, modelSelection=1), "", path_images)
facenet=FaceNet()
SVM_model=pickle.load(open(r'C:\Users\moham\PycharmProjects\FinalProject_Face_recognitions\Moldels\model_SVM.pkl', 'rb'))
emmbeading_model=np.load(r"..\Moldels\Model1.npz")
y=emmbeading_model['arr_1']
encoder= LabelEncoder().fit(y)
# its to recognition
threshold=0.5

def main(path_vidio):
    cap = cv2.VideoCapture(0)
    resoult=[]
    while cap.isOpened():
        ret, frame = cap.read()
        resoult = model.face_detection(frame)
        for face , (x, y, w, h) in resoult:
            ypred=facenet.embeddings(face)
            face_name=SVM_model.predict(ypred)
            popabilty=SVM_model.predict_proba(ypred)
            final_naem=encoder.inverse_transform(face_name)
            max_propablity=max(popabilty[0])
            if max_propablity < threshold:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cvzone.putTextRect(frame, " UNkoun ,Score : {}%".format(popabilty[0]), (x, y - 10),
                                   scale=1, thickness=1)
            else :
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cvzone.putTextRect(frame, " {} ,Score : {}%".format(final_naem,max_propablity), (x, y - 10),scale=1, thickness=1)

            print("************************resoult************************  ",final_naem)

        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("t"):
            cap.release()
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            break
    if cv2.waitKey(0):
       cap.release()
def take_sample_image_to_all_vedious():
    for vedio in os.listdir(r"..\vedious"):
        model.take_a_sample_from_vidio(os.path.join(r"..\vedious", vedio))


if __name__ == "__main__":
    video_path = r"C:\Users\moham\PycharmProjects\FinalProject_Face_recognitions\vedious\ahmad.mp4"  # your video file path will be set here
    main(video_path)






