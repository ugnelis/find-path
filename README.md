# find-path
Find Path project finds humans paths and routes, such as sidewalks, park ways, forest paths. This project implements semantic segmentation approach. It uses VGG16 pretrained model.

[![Semantic Segmentation - Ugnius Malūkas](https://img.youtube.com/vi/jTj_mzeoVm0/0.jpg)](https://www.youtube.com/watch?v=jTj_mzeoVm0)

## Path Finding 
### Installation 
TODO

### Training
Go to *calculations* folder.
```bash
$ cd calculations
```
Run training.
```bash
$ python train.py
```
### Run Trained Model
Check for examples in *calculations/demo.py*, *calculations/demo.ipynb*, *calclulations/video_demo.ipynb* files.

## Dataset Maker
For making dataset, web based application was made which uses just JavaScript without any framework.

### Installation
Before installation, make sure that NodeJS, npm and bower are installed.
```bash
$ cd dataset_maker
$ install bower
```

### Launching
Open *index.html* and have fun.

## Dataset
All dataset images have 320 widht, 180 height and contain 3 channels. Every image has own *.json* file which describes object in the image. In this project only 3 classes are observed: **boundaries** (everything arround path), **paths / ways** and **obstacles** (things that are on path - eg. human, road pit and etc.). Dataset contains 300 images (I'll a bit later).

## Path Finding with OpenCV
Check *calculations/cv/* folder.

## Code References
https://github.com/MarvinTeichmann/tensorflow-fcn
https://github.com/shelhamer/fcn.berkeleyvision.org
https://github.com/machrisaa/tensorflow-vgg
