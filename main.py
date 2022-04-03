import cv2 as cv
import time
import datetime

capture = cv.VideoCapture(0)

face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_fullbody.xml")

detect = False
detect_stop_t = None
timer_start = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(capture.get(3)), int(capture.get(4)))
fourcc = cv.VideoWriter_fourcc(*"mp4v")

while True:
    _, frame = capture.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detect:
            timer_start = False
        else:
            detect = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv.VideoWriter(
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")
    elif detect:
        if timer_start:
            if time.time() - detection_stop_t >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detect = False
                timer_start = False
                out.release()
                print('Stop Recording!')
        else:
            timer_start = True
            detection_stop_t = time.time()

    if detect:
        out.write(frame)

        for (x, y, width, height) in faces:
            cv.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
        for (x, y, width, height) in bodies:
            cv.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    cv.imshow("Security - Camera", frame)

    if cv.waitKey(1) == ord('q'):
        break

out.release()
capture.release()
cv.destroyAllWindows()