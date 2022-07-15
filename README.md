# 🌱Plant Diagnosis Detection

_Identifying plants and diagnosing various issues with them._
[Github](https://github.com/organization-x/omni/issues).

### What is it and Why?🤔

The main goal of this Plant Diagnosis Detection is to help general consumers understand what health issues are affecting their plant and to revive it as soon as possible! This AI product is able to identify the type of plant and then detect the particular disease it is experiencing based on the type of plant. At the moment, the AI supports a total of 14 species of plants to identify and about 35 diseases for all of the plants cumulatively. 

### Work Process 💻

This AI product runs on the YOLOv5 Algorithm Object Detection Model in which identifies the plants and individual diseases also. The steps are described below:

  1. Scraping data with SerpAPI and Python's Beautiful Soup HTML parser for the plants and various diseases
  2. Labeling and cleaning the data with RoboFlow software for getting ready to train our final models. One project for the identification and separate projects had been created, resulting in about 13,500+ images in total
  3. Exporting and augmenting our data into the YOLOv5 model for higher accuracy and strength within the product
  4. Model training through Google Colab that included an external GPU, RAM, and Disk Memory --> Inputting data accordingly
  5. Using Python Flask as the backend and frontend applications such as HTML, CSS, and Bootstrap, our website was developed. The linking process included PyTorch files for each model directly from YOLOv5
  

### 👏The Team👏

**Jinxuan Tang: Professor and Instructor**

**Srikar Vemuri**

**Ben Buzard**

**Isabelle Sebastian**

**Ashley Ko**

**Justin Erdenebileg**

**Nathan Zhou**

<!-- ### Usage🚀

First clone this repository through 

`https://github.com/organization-x/omni`

cd into the `/app` folder

`python3 -m pip install -r requirements.txt`

edit line 29 the `main.py` file to either the URL of the cocalc server you are on or `localhost` if you are running it on your own PC

Then, clone ultralytics yolov5 in the app folder, by running 

`git clone https://github.com/ultralytics/yolov5`
`pip install -r yolov5/requirements.txt`

Run

 `python3 -main.py`

to start the server on local, most changes while developing will be picked up in realtime by the server -->

### Statistics📈

The stats include graphs and matrices of the identification and working diagnosis projects for 10 plants specifically. [Diagnosis Confusion Matrix Folder](https://drive.google.com/drive/folders/1d2rJ411F4MO6CYwUYqsSeXC-8mZteS77?usp=sharing "Diagnosis")

**Identification Confusion Matrix:**
![](https://github.com/Plant-Identification-and-Diagnosis-AI/SC22-BatchB-DynamiteDuelers-PlantIdentificationAndDiagnosis/blob/omni_cv/app/static/images/confusion_matrixes/confusion_matrix.png?raw=true)


**RoboFlow Stats:**
![](https://github.com/Plant-Identification-and-Diagnosis-AI/SC22-BatchB-DynamiteDuelers-PlantIdentificationAndDiagnosis/blob/omni_cv/app/static/images/roboflow_stats.png?raw=true)


**Metrics:**
![](https://github.com/Plant-Identification-and-Diagnosis-AI/SC22-BatchB-DynamiteDuelers-PlantIdentificationAndDiagnosis/blob/omni_cv/app/static/images/results.png?raw=true)


## 😊Thank You!😊
Everything hosted by the [AI Camp Organization](ai-camp.org "AI Camp"). An amazing experience that every student absolutely should immerse themselves into. Thank You once again!