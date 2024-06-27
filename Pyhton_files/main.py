from Pyhton_files.class_.ModelRecognitionAndDtection import ModelRecognitionAndDtection1 as mymodel
from cvzone.FaceDetectionModule import FaceDetector
def main(path_vidio):
    path_images= r"..\Colect_Data\all_images"
    model = mymodel("",FaceDetector,"",path_images)
    model.take_a_sample_from_vidio(path_vidio)

if __name__ == "__main__":
    video_path = r"C:\Users\moham\PycharmProjects\FinalProject_Face_recognitions\vedious\ahmad.mp4"  # your video file path will be set here
    main(video_path)

