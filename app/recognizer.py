import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
from app.database import insert_attendance, check_duplicate


def start_attendance():

    # Load trained encodings
    with open("data/encodings.pickle", "rb") as f:
        data = pickle.load(f)

    known_encodings = data["encodings"]
    known_names = data["names"]

    video = cv2.VideoCapture(0)

    def mark_attendance(name):
        today = datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.now().strftime("%H:%M:%S")

        # Prevent duplicate attendance
        if check_duplicate(name, today):
            return

        insert_attendance(name, today, time_now)

    print("Starting webcam... Press ENTER to exit.")

    while True:
        ret, frame = video.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):

            face_distances = face_recognition.face_distance(known_encodings, encoding)

            if len(face_distances) == 0:
                continue

            best_match_index = np.argmin(face_distances)
            confidence = (1 - face_distances[best_match_index]) * 100

            if face_distances[best_match_index] < 0.60:
                name = f"{known_names[best_match_index]} ({confidence:.2f}%)"
                mark_attendance(known_names[best_match_index])
            else:
                name = "Unknown"

            top, right, bottom, left = location
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Smart Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == 13:
            break

    video.release()
    cv2.destroyAllWindows()