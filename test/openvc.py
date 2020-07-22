import cv2

cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier(r'D:\program\demoworkspace\opencv-4.3.0\data\haarcascades\haarcascade_frontalface_default.xml')  #待更改
#为即将录入的脸标记一个id
face_id = 12
#sampleNum用来计数样本数目
count = 0


while True:
    #从摄像头读取图片
    success, img = cap.read()
    #转为灰度图片，减少程序符合，提高识别度
    if success is True:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        break
    #检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
    #其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        cv2.imwrite("kk.jpg", img)
        index = index + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#关闭摄像头，释放资源
cap.realease()
cv2.destroyAllWindows()