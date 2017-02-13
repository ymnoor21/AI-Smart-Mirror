import sys, os
import numpy as np
import subprocess
import paramiko
from PIL import Image
from config import Config

vision_enabled = False
try:
    import cv2
    import cv2.face
    vision_enabled = True
except Exception as e:
    print("Warning: OpenCV not installed. To use facial recognition, make sure you've properly configured OpenCV.")


class Vision(object):
    def __init__(self, facial_recognition_model="models/facial_recognition_model.xml", camera=0):
        self.facial_recognition_model = facial_recognition_model
        self.camera = camera

    def detect_face(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)
        flag = False

	# Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            if x > 0 and y > 0 and w > 0 and h > 0:
                flag = True
            else:
                flag = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            flag = False

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
        return flag

    def detect_face_with_ractangle(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

    def create_face_dataset(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)
        id = raw_input("Enter user id: ")
        counter = 0

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                counter = counter + 1
                cv2.imwrite('models/userimages/user.' +
                            str(id) + "." + 
                            str(counter) + ".jpg", 
                            gray[y:y+h, x:x+w])

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(100)

            # Display the resulting frame
            cv2.imshow('Video', frame)
            cv2.waitKey(1)

            if counter >= 20:
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

    def train_recognizer(self):
        recognizer = cv2.face.createLBPHFaceRecognizer()
        file_path = 'models/userimages'

        imagePaths = [
            os.path.join(file_path, f) 
            for f in os.listdir(file_path) 
            if f not in ['.DS_Store', '.gitignore']
        ]
        faces = []
        IDs = []

        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        
        recognizer.train(faces, np.array(IDs))
        recognizer.save('models/recognizer/trainningData.yml')
        cv2.destroyAllWindows()

    def identify_face_lbph(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)

        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.load("models/recognizer/trainningData.yml")

        id = 0

        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                if id == 1:
                    name = "Yamin"
                elif id == 2:
                    name = "Sadia"
                elif id == 3:
                    name = "Omi"
                elif id == 4:
                    name = "Ankhi"
                else:
                    name = "Unknown"

                print(id, name, conf)

                cv2.putText(frame, str(name), (x, y+h+30), font, 1, (255, 0, 0), 2)
            
            cv2.imshow('Face', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def identify_face2_svm(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)

        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.load("models/recognizer/trainningData.yml")

        id = 0

        font = cv2.FONT_HERSHEY_SIMPLEX

        # while True:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        people = []

        for (x, y, w, h) in faces:
            img_name = 'models/tmpimages/user.' + str(id) + ".jpg"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(img_name, gray[y:y+h, x:x+w])

            docker_command = "docker exec -it " + \
                Config.OPENFACE_DOCKER_CONTAINER_ID + \
                " /bin/bash " \
                "-c \"cd /root/openface && " \
                "./demos/classifier.py infer " \
                "./generated-embeddings/classifier.pkl " \
                "/host/Users/" + img_name + "\""
            
            p = subprocess.Popen(
                    docker_command, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT
                )

            for line in p.stdout.readlines():
                if "Predict" in line:
                    literals = line.split(" ")

                    people.append({
                        'name': literals[1],
                        'confidence': literals[3],
                    })

        cv2.imshow('Faces', frame)

        video_capture.release()
        cv2.destroyAllWindows()

        return people

    def identify_face_by_linearsvm2(self):
        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)

        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.load("models/recognizer/trainningData.yml")

        id = 0

        font = cv2.FONT_HERSHEY_SIMPLEX

        # while True:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        people = []
        imagepath = []

        remotepath = Config.FR_PC_IMG_UPLOAD_PATH

        for (x, y, w, h) in faces:
            image = Config.IMG_SAVE_PATH + '/user.' + str(id) + ".jpg"
            imagepath.append(Config.DOCKER_HOST_IMG_PATH + '/user.' + str(id) + '.jpg')
            cv2.imwrite(image, gray[y:y+h, x:x+w])

        os.system("scp -r " + Config.IMG_SAVE_PATH + "/* " + 
            Config.FR_PC_USER + "@" + Config.FR_PC_HOST + ":" + remotepath)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(Config.FR_PC_HOST, username=Config.FR_PC_USER, password=Config.FR_PC_PASS)

        images = (imagepath.join(" ") if len(imagepath) > 1 else imagepath[0])

        stdin, stdout, stderr = client.exec_command(
            'docker exec -i ' + Config.OPENFACE_DOCKER_CONTAINER_ID + 
            ' /bin/bash -c "cd /root/openface && ./demos/classifier.py infer '
            './generated-embeddings/classifier.pkl ' + images + '"'
        )

        for line in stdout:
            strippedLine = line.strip('\n')
            if "Predict" in strippedLine:
                splitLine = strippedLine.split(" ")
                people.append({'name': splitLine[1], 'confidence': splitLine[3]})

        client.close()

        video_capture.release()
        cv2.destroyAllWindows()

        return people

    def recognize_face(self):
        """
        Wait until a face is recognized. If openCV is configured, always return true
        :return:
        """

        if vision_enabled is False:  # if opencv is not able to be imported, always return True
            return True

        face_cascade = cv2.CascadeClassifier(self.facial_recognition_model)
        video_capture = cv2.VideoCapture(self.camera)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces) > 0:
                # When everything is done, release the capture
                video_capture.release()
                cv2.destroyAllWindows()

                return True


if __name__ == "__main__":
    v = Vision()
    # print(v.detect_face())
    # v.create_face_dataset()
    # v.train_recognizer()
    # v.identify_face()
    # v.identify_face_by_linearsvm2()
