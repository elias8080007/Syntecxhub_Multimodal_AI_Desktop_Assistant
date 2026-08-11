import cv2


def run_face_gate(
    camera_index=0,
    required_frames=20
):
    cascade_path = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    face_detector = cv2.CascadeClassifier(
        cascade_path
    )

    if face_detector.empty():
        print("Error: Face detection model could not be loaded.")
        return False

    camera = cv2.VideoCapture(
        camera_index,
        cv2.CAP_DSHOW
    )

    if not camera.isOpened():
        print("Error: The webcam could not be opened.")
        return False

    stable_frames = 0
    access_granted = False

    print("Face-detection access gate started.")
    print("Look toward the camera.")
    print("Press Q to cancel.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read a webcam frame.")
                break

            frame = cv2.flip(frame, 1)

            grayscale_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                grayscale_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )

            if len(faces) > 0:
                stable_frames = min(
                    stable_frames + 1,
                    required_frames
                )

                status_text = "Face detected"
                status_color = (0, 255, 255)

            else:
                stable_frames = max(
                    stable_frames - 2,
                    0
                )

                status_text = "No face detected"
                status_color = (0, 0, 255)

            for x_position, y_position, width, height in faces:
                cv2.rectangle(
                    frame,
                    (x_position, y_position),
                    (
                        x_position + width,
                        y_position + height
                    ),
                    (0, 255, 0),
                    3
                )

            progress = (
                stable_frames / required_frames
            )

            bar_x = 20
            bar_y = 90
            bar_width = 300
            bar_height = 25

            completed_width = int(
                bar_width * progress
            )

            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                status_color,
                2
            )

            cv2.putText(
                frame,
                (
                    f"Authentication progress: "
                    f"{progress:.0%}"
                ),
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (
                    bar_x + bar_width,
                    bar_y + bar_height
                ),
                (255, 255, 255),
                2
            )

            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (
                    bar_x + completed_width,
                    bar_y + bar_height
                ),
                (0, 255, 0),
                -1
            )

            cv2.putText(
                frame,
                "Press Q to Cancel",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            if stable_frames >= required_frames:
                access_granted = True

                cv2.putText(
                    frame,
                    "ACCESS GRANTED",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1,
                    (0, 255, 0),
                    3
                )

                cv2.imshow(
                    "AI Assistant - Face Access Gate",
                    frame
                )

                cv2.waitKey(1000)
                break

            cv2.imshow(
                "AI Assistant - Face Access Gate",
                frame
            )

            pressed_key = (
                cv2.waitKey(1) & 0xFF
            )

            if pressed_key == ord("q"):
                print("Face gate cancelled by the user.")
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    if access_granted:
        print("Access granted successfully.")
    else:
        print("Access was not granted.")

    return access_granted


if __name__ == "__main__":
    result = run_face_gate()

    print(
        f"Face gate result: {result}"
    )