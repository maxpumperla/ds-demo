# Security camera demo using object detection with YOLOv3. Built with Plotly Dash, Flask and Keras

The material found in this folder was used for a quick 45 minute demo
to illustrate what data science might mean in practice.

## Quick Start

The yolo model used in this demo is based on [this project](https://github.com/qqwweee/keras-yolo3).
Start from a fresh Python 3.6 virtual environment and install all requirements for this project.

```bash
virtualenv venv -p python3.6 && source venv/bin/activate
pip install -r requirements.txt
```

Next, download YOLOv3 weights from [YOLO website](http://pjreddie.com/darknet/yolo/)
and convert the Darknet YOLO model to a Keras model and Keras weights

```bash
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
python convert.py -w yolov3.cfg yolov3.weights model_data/yolo_weights.h5
```

For model training you need to download and unzip 
[PASCAL VOC 2007 training data](http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar) first.

Make sure the folder `VOCdevkit` is placed next to this readme file.

## YOLO training

To learn more about YOLO training, start a jupyter notebook server locally

```bash
jupyter-notebook .
```

open `YOLO_training.ipynb` and follow the notebook. If you want to track
your model training with Google TensorBoard, make sure to run

```bash
./tensorboard.sh
```

before starting training in the notebook. You can see training progress and
YOLO network architecture on `localhost:6006`.


## Security camera demo

To start a little security camera demo that can detect whenever an intruder
(which we made out to be a `banana`) enters your webcam, first start the
Python backend with

```bash
python yolo_video.py
```

If you've run this demo before make sure to delete the generated `payload.json`
before starting `yolo_video.py`.

The security dashboard itself is started with the following command:

```bash
python app.py
```

which starts the demo in your browser at `http://127.0.0.1:8050/`.

