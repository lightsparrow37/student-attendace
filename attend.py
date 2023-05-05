# Import required libraries
import cv2
import face_recognition
import numpy as np

# Load a sample image and encode it
known_image = face_recognition.load_image_file("known_face.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize variables
students = ["Alice", "Bob", "Charlie"] # List of student names
present_students = [] # List of students present

# Initialize video capture from default camera
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = video_capture.read()

    # Convert the frame to RGB format for face_recognition library
    rgb_frame = frame[:, :, ::-1]

    # Find all faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Check if each face matches the known face encoding
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
        name = "Unknown" # Default name if face is not recognized

        # If face matches known face encoding, get the student name
        if True in matches:
            index = matches.index(True)
            name = students[index]

            # Add the student to the list of present students if not already added
            if name not in present_students:
                present_students.append(name)

        # Draw a rectangle around the face and display the name
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Display the frame
    cv2.imshow('Video', frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
video_capture.release()
cv2.destroyAllWindows()

# Print the list of present students
print("Present students:")
for student in present_students:
    print(student)
