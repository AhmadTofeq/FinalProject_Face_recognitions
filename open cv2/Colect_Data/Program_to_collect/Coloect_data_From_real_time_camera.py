from cvzone.FaceDetectionModule import FaceDetector
import cvzone
import cv2
####################################variables
floating_point=5
path_save_image_all= r"/Colect_Data/all_images/"
accept_fake_and_real=True
#############################################


def main():

    # Initialize the webcam
    # '2' means the third camera connected to the computer, usually 0 refers to the built-in webcam
    cap = cv2.VideoCapture(0)
    # Initialize the FaceDetector object
    # minDetectionCon: Minimum detection confidence threshold
    # modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
    detector = FaceDetector(minDetectionCon=0.3, modelSelection=1)

    # Run the loop to continually get frames from the webcam
    while True:
        # Read the current frame from the webcam
        # success: Boolean, whether the frame was successfully grabbed
        # img: the captured frame
        success, img = cap.read()

        # Detect faces in the image
        # img: Updated image
        # bboxs: List of bounding boxes around detected faces
        img, bboxs = detector.findFaces(img, draw=False)

        # Check if any face is detected
        if bboxs:
            # Loop through each bounding box
            for bbox in bboxs:
                # bbox contains 'id', 'bbox', 'score', 'center'

                # ---- Get Data  ---- #
                center = bbox["center"]
                x, y, w, h = bbox['bbox']
                score = int(bbox['score'][0] * 100)

                # ---- Draw Data  ---- #
            #----------------------- Defult rectange and score above rectaqngel ---------------------------
                # cv2.circle(img, center, 5, (255, 0, 255) , cv2.FILLED)
                #
                # cvzone.putTextRect(img, f'{score}%', (x, y ))
                # cvzone.cornerRect(img, (x, y, w, h))
            # ----------------------------------create my own custom rectange and drw it -----------------------------------
                # it used to change size rectangle and create a custom rectangle
                x -= int(w * 0.2)
                w+=int((w * 0.2)*1.5)
                y-=int((h*0.5))
                h += int((h * 0.5)*1.3)

            #------------------------------------ to avoidind value of x,y,w.h  is not gonna be below zero for that we have to --------------------------------
                if x<0:x=0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

            #----------------------------------- find picture bluriness -----------------------------------------------
              #***** show those face that you detecteed******
                image_face=img[y:y+h,x:x+w]
                cv2.imshow("face",image_face)
                fac_blur_raite=int(cv2.Laplacian(image_face,cv2.CV_64F).var())
                if fac_blur_raite>150:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
                    cvzone.putTextRect(img,"fake face blure :{} ,Score : {}%".format(fac_blur_raite,score),(x,y-10),scale=1, thickness=1)

                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
                    cvzone.putTextRect(img,"real face blure :{} ,Score : {}%".format(fac_blur_raite,score),(x,y-10),scale=1, thickness=1)
            #----------------------------------- Normalization image  -----------------------------------------------
                # print(f"x={x} , y={y}, w={w} ,h={h}")
                wi,hi,_=img.shape
                xc,yc=x+w/2,y+h/2
                xcn,ycn=round(xc/wi,floating_point),round(yc/hi,floating_point)
                wn,hn=round(w/wi,floating_point),round(h/hi,floating_point)
                # print(f"xcn={xcn} , ycn={ycn}  , wN= {wn}  , yn ={yn}" )
                # print(f"wi={wi} , hi={hi}")
                # ------------------------------------ to avoidind value of xn,yn,wn,hn  is not gonna be above 1 for that we have to --------------------------------
                if xcn > 1: xcn = 1
                if ycn >1: ycn = 1
                if wn >1: wn = 1
                if hn >1: hn = 1
            # ------------------------------------ Save image in all_image directory --------------------------------
                if accept_fake_and_real:
                   cv2.imwrite(f"{path_save_image_all}{xcn, ycn, wn, hn}.jpg", image_face)
                else:
                   if fac_blur_raite<150:
                       cv2.imwrite(f"{path_save_image_all}{xcn, ycn, wn, hn}.jpg", image_face)
        # Display the image in a window named 'Image'
        cv2.imshow("Image", img)
        # Wait for 1 millisecond, and keep the window open

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.release()
            break


if __name__ == "__main__":
    main()