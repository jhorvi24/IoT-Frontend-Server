from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import csv
from datetime import datetime
import pytz
import math

app = Flask(__name__)
CORS(app)




def save_to_csv(temperature, humidity):
    with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ['time','temperature', 'humidity']  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  

        # Check if the file is empty to write header  
        csvfile.seek(0, 2)  # Move the cursor to the end of the file  
        if csvfile.tell() == 0: # If file is empty, write header
            writer.writeheader()
        
        timezone = pytz.timezone("America/Bogota")
        now = datetime.now(timezone)
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        writer.writerow({'time': formatted_time, 'temperature': temperature, 'humidity': humidity})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data_received():
    humidity = request.form['humidity']
    temperature = request.form['temperature']
    print(f"Humidity: {humidity}%, temperature: {temperature}°C")
    save_to_csv(temperature,humidity)

    return 'Data received', 200

@app.route('/temperature')
def get_temperature():
    data = []
    with open('data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:

            try:

                temp = float(row['temperature'])
                hum = float(row['humidity'])
                # Solo añadir si los valores son válidos

                if math.isnan(temp) and math.isnan(hum):
                    continue
                values ={
                    'time': row['time'],
                    'temperature': temp,
                    'humidity': hum
                }

                data.append(values)
                
                
            except (ValueError, TypeError):
                    continue
    
    return jsonify(data)
    
    
      
    

@app.route('/test')
def test():
    return "Hello from Gitpod"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)