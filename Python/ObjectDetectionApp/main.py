import time
import sys
import random

def run_simulation():
    print("--- SIMULATION MODE ACTIVATED ---")
    print("(OpenCV not found. Install it via 'pip install opencv-python' to run real detection)")
    print("Initializing Camera Hook in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Camera simulated. Scanning for objects...")
    
    objects = ["Person", "Cat", "Dog", "Car", "Chair", "Laptop"]
    
    start_time = time.time()
    while True:
        try:
            detected = random.choice(objects)
            confidence = random.uniform(85.0, 99.9)
            
            print(f"[{time.strftime('%H:%M:%S')}] DETECTED: {detected} | Confidence: {confidence:.2f}%")
            time.sleep(random.uniform(1.5, 3.0))
            
            if time.time() - start_time > 15: # Run for 15 seconds
                print("\nSimulation ended. Exiting...")
                break
        except KeyboardInterrupt:
            print("\nStopped.")
            break

def run_real_detection():
    import cv2
    
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)
    
    print("Press 'q' to stop.")
    
    while True:
        # Read the frame
        _, img = cap.read()
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
            
        # Display
        cv2.imshow('Object Detection App - Face', img)
        
        # Stop if q key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Welcome to Object Detection App 2025")
    try:
        import cv2
        print("OpenCV detected. Starting Real Detection Mode...")
        run_real_detection()
    except ImportError:
        print("OpenCV NOT found.")
        run_simulation()

if __name__ == "__main__":
    main()
