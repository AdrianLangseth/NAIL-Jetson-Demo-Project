# NAIL-Jetson-Demo-Project

NAIL-Jetson-Demo-Project is a Python project in relation to my summer internship at the Norwegian AI Lab (NAIL) at NTNU.
This project is made to work on the SparkFun JetBot AI Kit, with the final product being a showcase of different AI tools in a relatable setting.
My approach was to emulate and win a game of [Hide and Seek](https://en.wikipedia.org/wiki/Hide-and-seek) against inanimate objects, within the [COCO dataset](https://cocodataset.org/).
This was achieved using a hierarchical combination of Monocular Depth Estimation, Object Detection and Collision Avoidance. Object Detection owning override on the other two modules, Collision Avoidance owning override on Monocular Depth Estimation, and Monocular Depth Estimation always running until told otherwise.




## ⚙️ Setup

This project builds on the [Niantic Monodepth2 repository](https://github.com/nianticlabs/monodepth2). Cloning these are therefore necessary for full functionality.

The directory has a `requirements.txt` file which can be used to install all necessary components. This is done in the terminal as such:
`pip3 install requirements.txt`
However, the Jetson Nano is extremely opposed to virtual environments and would not allow any workaround. In addition to this, I only had access to one Jetbot. Therefore, the generated requirements file contained all modules of the Jetbot and jetson itself and had to be trimmed manually. Therefore, this leaves room for human error in the conciseness and completeness of the `requirements.txt` file.



#### 📁 File Structure

The file structure used to complete the project is as follows:

```
Home folder    
│
└───Hide 'n' Seek Project Directory
│   │   main.ipynb
│   │   main.py
│   │   coco_labels.txt
│   │   README.md
│   │   best_model.pth
│   │   README.md
│   │
│   └───models
│       └───mono_640x192
│           .
|           .
│           .
|           .
│   
└───monodepth2
│   .
│   .
│
└───jetson-inference
|   .
│   .
│
└───jetbot
    .
    .
```

## Running

The program can be run a Jupyter Notebook as well as a python script. Inexplicably, the Jupyter Notebook is orders of magnitude faster than the python file.

To run through the python script, all you need to do is enter the Hide 'n' Seek project directory, and run the main.py file:

`$ python3 main.py`

To run through the Jupyter Notebook, one would first have to enter the project directory and boot up Jupyter Notebook:

`Hide-and-seek-Directory$ jupyter notebook`

## ⭐️ Acknowledgements
- [nianticlabs](https://github.com/nianticlabs)
- [dustynv](https://github.com/dustynv)

## Model Changes
- The Collision Avoidance model has been pre-trained on the COCO Dataset, and further trained on the specific Lab room.
- The Monocular depth perception model is unchanged from the

## Built With
- [Niantic Monodepth2 repository](https://github.com/nianticlabs/monodepth2)
- NVIDIA Collision Avoidance and Object Following Examples](https://github.com/NVIDIA-AI-IOT/jetbot)

## Known Issues / fix

When the GPU gets overwhelmed with work, it tends to stop updating the camera values. This may perpetuate after the load is lightened and even after restarting the program and system. The only working fix I found was restarting the nvargus-daemon. This is done by running this line in the console:

`$ sudo systemctl restart nvargus-daemon`

The Jetson Nano using the [Raspberry Pi NoIR Camera V2](https://www.raspberrypi.org/products/pi-noir-camera-v2/) is extremely near-sighted when it comes to object recognition. It accurately and notices objects within ~25cm. This applies for all feasible resolutions. This can be fixed by running on better hardware.

The Jetson Nano is extremely opposed to virtual environments. Every

## ⏭ ToDo
The file structure is a mess. I got too deep into the web before I found that I would be the only one able to understand how it is connected, and now its been a month since I last looked at it and cannot remember a thing.

## Disclaimer
This code is used only non-commercially, following the licensing of Niantic Monodepth2.
