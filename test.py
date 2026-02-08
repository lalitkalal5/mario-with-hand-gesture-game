from hand_detector import HandDetector
det = HandDetector("hand_landmarker.task")

while True:
    hand_up, hand_y = det.get_hand_up()

    print("hand_up", hand_up, "y:", hand_y)

det.close()
