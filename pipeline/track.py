from ultralytics import YOLO
import cv2
import requests
from datetime import datetime
import uuid


model = YOLO("yolov8n.pt")


def run_tracking(video_path):

    print("Opening video:", video_path)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("ERROR: Cannot open video")
        return

    counted_ids = set()

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Finished reading video")
            break

        results = model.track(
            frame,
            persist=True,
            classes=[0]
        )

        annotated_frame = results[0].plot()

        if results[0].boxes.id is not None:

            track_ids = results[0].boxes.id.int().cpu().tolist()

            for track_id in track_ids:

                if track_id not in counted_ids:

                    counted_ids.add(track_id)

                    event = {
                        "event_id": str(uuid.uuid4()),
                        "store_id": "ST1008",
                        "camera_id": "CAM01",
                        "visitor_id": str(track_id),
                        "event_type": "entry",
                        "timestamp": str(datetime.now()),
                        "confidence": 0.95
                    }

                    try:

                        response = requests.post(
                            "http://127.0.0.1:8000/events/ingest",
                            json=[event]
                        )

                        print(
                            f"Visitor {track_id} sent:",
                            response.json()
                        )

                    except Exception as e:
                        print("API Error:", e)

        visitor_count = len(counted_ids)

        cv2.putText(
            annotated_frame,
            f"Visitors: {visitor_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Store Tracking",
            annotated_frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()