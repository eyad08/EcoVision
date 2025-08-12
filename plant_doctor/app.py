from flask import Flask, request, render_template
import cv2
import numpy as np

app = Flask(__name__)

def analyze_colors(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.count_nonzero(green_mask) / (img.shape[0] * img.shape[1])
    green_percent = round(green_ratio * 100, 2)
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_ratio = np.count_nonzero(yellow_mask) / (img.shape[0] * img.shape[1])
    yellow_percent = round(yellow_ratio * 100, 2)
    
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([20, 255, 200])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    brown_ratio = np.count_nonzero(brown_mask) / (img.shape[0] * img.shape[1])
    brown_percent = round(brown_ratio * 100, 2)
    return green_percent, yellow_percent, brown_percent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])  
def upload():
    if 'file' not in request.files:
        return "لا توجد صورة مرفوعة!"
    file = request.files['file']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    green, yellow, brown = analyze_colors(img)
    return render_template('result.html', green=green, yellow=yellow, brown=brown)

if __name__ == '__main__':
    app.run(debug=True)
