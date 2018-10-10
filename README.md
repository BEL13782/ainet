# Introduction
This application runs a tensorflow/opencv module for object detection and image processing, and a django web module for interacting with the data output from the first module.
Neither of them can be run as standalone apps

# Prerequesites :

Windows 10 or Ubuntu 16.04

An Nvidia GPU with at least 768 Cuda Cores

Cuda toolkit version >= 9.0

CuDNN ver 7.5

Tensorflow >= 1.6.0

MongoDB 3.4

Please visit https://developer.nvidia.com/ for Cuda and CuDNN installation instructions
...




# Clone this repo and setup the environment
git clone https://github.com/BEL13782/ainet.git

# Download models
```
cd ainet
Download and extract the models manually or run setup.sh


```


| Model name  | Speed | COCO mAP | Outputs |
| ------------ | :--------------: | :--------------: | :-------------: |
| [ssd_mobilenet_v1_coco](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz) | fast | 21 | Boxes |
| [ssd_inception_v2_coco](http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_11_06_2017.tar.gz) | fast | 24 | Boxes |
| [rfcn_resnet101_coco](http://download.tensorflow.org/models/object_detection/rfcn_resnet101_coco_11_06_2017.tar.gz)  | medium | 30 | Boxes |
| [faster_rcnn_resnet101_coco](http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017.tar.gz) | medium | 32 | Boxes |
| [faster_rcnn_inception_resnet_v2_atrous_coco](http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017.tar.gz) | slow | 37 | Boxes |

# Download demo video
```
mkdir videos
Download and copy video https://www.dropbox.com/s/9qp095kv6a2slev/ab-easy2.mp4?dl=0
``` 

# Install dependecies
```
cd ..
pip install -r requirements.txt
```

# Setup and run the demo database
```
mongorestore -d testdb demodb
mongod
```






# Run Demo


```
# Specify or override the entry/exit line (can be skipped)
python line.py 5

# Start the demo
python engine.py

# Run the webapp and check the results
cd webapp
python manage.py runserver
Open browser and go to localhost:8000/ainet (username : test1 ; password : azerty01)

```

