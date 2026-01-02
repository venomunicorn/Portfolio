import time
import random

# Producer: Simulates a sensor generating data
def sensor_stream(n=20):
    for i in range(n):
        # Simulate data: {id, temp, status}
        temp = random.uniform(20.0, 100.0)
        yield {
            'id': i,
            'timestamp': time.time(),
            'temperature': temp,
            'status': 'OK' if temp < 90 else 'CRITICAL'
        }
        time.sleep(0.1)  # Simulate delay

# Processing Stage 1: Filter
def filter_critical(stream):
    for data in stream:
        if data['status'] == 'CRITICAL':
            yield data

# Processing Stage 2: Transform (e.g., Fahrenheit conversion)
def to_fahrenheit(stream):
    for data in stream:
        data['temperature_f'] = (data['temperature'] * 9/5) + 32
        yield data

# Consumer: Actions
def alert_system(stream):
    print("--- Starting Monitoring Stream ---")
    for data in stream:
        print(f"[ALERT] High Temp Detected! ID:{data['id']} "
              f"Temp:{data['temperature']:.1f}C / {data['temperature_f']:.1f}F")

def main():
    print("Initializing Data Pipeline...")
    
    # 1. Source
    raw_data = sensor_stream(n=50)
    
    # 2. Pipeline Construction
    # Raw -> Critical Only -> Add Fahrenheit Units
    critical_data = filter_critical(raw_data)
    processed_data = to_fahrenheit(critical_data)
    
    # 3. Sink
    alert_system(processed_data)
    
    print("Stream ended.")

if __name__ == "__main__":
    main()
