import face_recognition
import os
import pickle
import cv2

def encode_faces():

    dataset_path = "data/dataset"

    print("Reading images from:", dataset_path)

    known_encodings = []
    known_names = []

    for image_name in os.listdir(dataset_path):
        print("Processing:", image_name)

        image_path = os.path.join(dataset_path, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print("Failed to load:", image_name)
            continue

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        encodings = face_recognition.face_encodings(rgb_image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(image_name)[0])
        else:
            print("No face detected in:", image_name)

    print("Total faces encoded:", len(known_names))

    data = {"encodings": known_encodings, "names": known_names}

    with open("data/encodings.pickle", "wb") as f:
        pickle.dump(data, f)

    print("Encodings saved successfully!")