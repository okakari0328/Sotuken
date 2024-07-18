import argparse
import cv2

def parse_args() -> tuple:
    parser = argparse.ArgumentParser(description="Capture video from camera or video file.")
    parser.add_argument("IN_CAM", help="Input camera number or video path", type=str)
    parser.add_argument("-f", "--FPS", help="Input FPS", type=float, default=None)
    args = parser.parse_args()
    return (args.IN_CAM, args.FPS)

def main() -> None:
    (in_cam, in_fps) = parse_args()
    
    if in_cam.isdigit():
        in_cam = int(in_cam)
    
    cap = cv2.VideoCapture(in_cam)
    
    # Get and set frame dimensions
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if frame_width != 640 or frame_height != 480:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Print frame dimensions
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"width:{frame_width}")
    print(f"height:{frame_height}")

    # Set camera properties
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_AUTO_WB, 1)

    # Set FPS if provided
    if in_fps is not None:
        cap.set(cv2.CAP_PROP_FPS, in_fps)
    print(f"fps:{cap.get(cv2.CAP_PROP_FPS)}")

    # Capture and display video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        cv2.imshow("output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
