from flask import send_from_directory
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import render_template
from url_utils import get_base_url
import os
import torch
import json
import urllib.parse
import cv2

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 25563
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

model_id = torch.hub.load("ultralytics/yolov5", "custom", path = 'ident.pt', force_reload=True)
model_toma = torch.hub.load("ultralytics/yolov5", "custom", path = 'toma.pt', force_reload=True)
model_grape = torch.hub.load("ultralytics/yolov5", "custom", path = 'grape.pt', force_reload=True)
model_apple = torch.hub.load("ultralytics/yolov5", "custom", path = 'apple.pt', force_reload=True)
model_blue = torch.hub.load("ultralytics/yolov5", "custom", path = 'blueberry.pt', force_reload=True)
# model_aloe =  torch.hub.load("ultralytics/yolov5", "custom", path = 'aloe.pt', force_reload=True)
model_snake = torch.hub.load("ultralytics/yolov5", "custom", path = 'snake.pt', force_reload=True)
model_orange = torch.hub.load("ultralytics/yolov5", "custom", path = 'orange.pt', force_reload=True)
# model_squash = torch.hub.load("ultralytics/yolov5", "custom", path = 'squash.pt', force_reload=True)
model_mango = torch.hub.load("ultralytics/yolov5", "custom", path = 'mango.pt', force_reload=True)
model_stra_rasp =  torch.hub.load("ultralytics/yolov5", "custom", path = 'straw_rasp.pt', force_reload=True)
model_pepper =  torch.hub.load("ultralytics/yolov5", "custom", path = 'pepper.pt', force_reload=True)
model_peach = torch.hub.load("ultralytics/yolov5", "custom", path = 'peach.pt', force_reload=True)
# model_cherry = torch.hub.load("ultralytics/yolov5", "custom", path = 'cherry.pt', force_reload=True)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_model(step, detected_plant):
    if step == 'plant':
        return model_id
    
    if detected_plant == "Tomato plant":
        return model_toma
    elif detected_plant == "Grape plant":
        return model_grape
    elif detected_plant == "Apple plant":
        return model_apple
    elif detected_plant == "Blueberry plant":
        return model_blue
    # elif detected_plant == "Aloe Vera":
    #     return model_aloe
    elif detected_plant == "Snake plant":
        return model_snake
    elif detected_plant == "Orange plant":
          return model_orange
    # elif detected_plant == "Squash plant":
    #     return model_squash
    elif detected_plant == "Mango plant":
        return model_mango
    elif detected_plant == "Strawberry plant" or "Raspberry plant":
        return model_stra_rasp
    elif detected_plant == "Pepper plant":
        return model_pepper
    elif detected_plant == "Peach plant":
        return model_peach
    # elif detected_plant == "Cherry plant":
    #     return model_cherry
    else:
        raise NotImplementedError(f"Unknown plant type: {detected_plant}")

@app.route(f'{base_url}', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    return render_template('home.html')


@app.route(f'{base_url}/use-model', methods=['GET', 'POST'])
def use_model():
    step = request.args.get('step')
    detected_plant = request.args.get('detected_plant')
    plant_confidence = request.args.get('plant_confidence')
    detected_disease = request.args.get('detected_disease')
    disease_confidence = request.args.get('disease_confidence')
    plant_filename = request.args.get('plant_filename')
    disease_filename = request.args.get('disease_filename')

    if request.method == 'POST':
        step = request.form['step']
        detected_plant = request.form['detected_plant']
        plant_confidence = request.form['plant_confidence']
        detected_disease = request.form['detected_disease']
        disease_confidence = request.form['disease_confidence']
        plant_filename = request.form['plant_filename']
        disease_filename = request.form['disease_filename']
        url = request.url.replace(("&" if "?" in request.url else "?") + "error=FILE_EXT_NOT_VALID", "")

        if 'file' not in request.files:
            flash('No file part')
            return redirect(url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url)

        if not allowed_file(file.filename):
            return redirect(url + ("&" if "?" in request.url else "?") + "error=FILE_EXT_NOT_VALID")

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename) + f"?step={step}&detected_plant={detected_plant}&plant_confidence={plant_confidence}&detected_disease={detected_disease}&disease_confidence={disease_confidence}&plant_filename={plant_filename}&disease_filename={disease_filename}")

    if 'error' in request.args:
        error = request.args.get('error')
    else:
        error = 'NONE'

    if 'filename' in request.args:
        filename = request.args.get('filename')
    else:
        filename = ''
    
    return render_template('use_model.html', error=error, filename=filename, step=step, detected_plant=detected_plant, plant_confidence=plant_confidence, detected_disease=detected_disease, disease_confidence=disease_confidence, plant_filename=plant_filename, disease_filename=disease_filename)


@app.route(f'{base_url}/uploads/<filename>')
def uploaded_file(filename):
    step = request.args.get('step')
    detected_plant = request.args.get('detected_plant')
    plant_confidence = request.args.get('plant_confidence')
    detected_disease = request.args.get('detected_disease')
    disease_confidence = request.args.get('disease_confidence')
    plant_filename = request.args.get('plant_filename')
    disease_filename = request.args.get('disease_filename')

    here = os.getcwd()
    image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)
    model = get_model(step, detected_plant)
    results = model(image_path, size=416)
    if len(results.pandas().xyxy) > 0:
        results.print()
        save_dir = os.path.join(here, app.config['UPLOAD_FOLDER'])
        results.save(save_dir=save_dir)
        filename = filename.replace(filename.split('.')[-1], filename.split('.')[-1].lower())
        image_path = os.path.join(here, app.config['UPLOAD_FOLDER'], filename)

        # img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        # resized = cv2.resize(img, (256, 256))
        # cv2.imwrite(image_path, resized)

        def and_syntax(alist):
            if len(alist) == 1:
                alist = "".join(alist)
                return alist
            elif len(alist) == 2:
                alist = " and ".join(alist)
                return alist
            elif len(alist) > 2:
                alist[-1] = "and " + alist[-1]
                alist = ", ".join(alist)
                return alist
            else:
                return
        confidences = list(results.pandas().xyxy[0]['confidence'])
        # confidences: rounding and changing to percent, putting in function
        format_confidences = []
        for percent in confidences:
            format_confidences.append(str(round(percent*100)) + '%')
        format_confidences = and_syntax(format_confidences)

        labels = list(results.pandas().xyxy[0]['name'])
        # labels: sorting and capitalizing, putting into function
        labels = set(labels)
        labels = [emotion.capitalize() for emotion in labels]
        labels = and_syntax(labels)

        print(labels)
        print(format_confidences)
        
        if step == 'plant':
            step = 'disease'
            detected_plant = labels
            plant_confidence = format_confidences
            plant_filename = filename
        elif step == 'disease':
            step = 'finish'
            detected_disease = labels
            disease_confidence = format_confidences
            disease_filename = filename
        else:
            print("person somehow broke this")

        return redirect(url_for('use_model', plant_filename=plant_filename, disease_filename=disease_filename, step=step, detected_plant=detected_plant, plant_confidence=plant_confidence, detected_disease=detected_disease, disease_confidence=disease_confidence))
        
    else:
        found = False
        return redirect(url_for('use_model', error="NOT_FOUND", filename=filename, step=step, detected_plant=detected_plant, plant_confidence=plant_confidence, detected_disease=detected_disease, disease_confidence=disease_confidence))


@app.route(f'{base_url}/uploads/<path:filename>')
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'https://cocalc15.ai-camp.dev'
    
    print(f'Try to open\n\n    {website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
