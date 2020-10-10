# NAIL-Jetson-Demo-Project

NAIL-Jetson-Demo-Project is a Python project in relation to my summer internship at the Norwegian AI Lab (NAIL) at NTNU.
This project is made to work on the SparkFun JetBot AI Kit, with the final product being a showcase of different AI tools in a relatable setting.
My approach was to emulate a game of [Hide and Seek](https://en.wikipedia.org/wiki/Hide-and-seek) against inanimate objects, within the [COCO dataset](https://cocodataset.org/).
This was achieved using a hierarchical combination of Monocular Depth Estimation, Object Detection and Collision Avoidance. Object Detection owning override on the other two modules, Collision Avoidance owning override on Monocular Depth Estimation, and Monocular Depth Estimation always running until told otherwise.
The approach of the program is to roam the free area with adaptive speed and direction based on the depth estimation, with a safety measure of the collision detection, which influences the motor functions passed from the depth estimation. Meanwhile the object detection module also reads off the camera values and perceives if an object of a type contained in the _accepted_classes_ list is within view. If so it overrides and disables the other modules, and approaches the object. In the off-chance the robot changes its mind whether an object of acceptable class is within FOV, it will resume its previously disabled processes of roaming. If it does not change its mind, it will continue driving to the hider and upon reaching the hider the game is won, and the program is finished.

## ⚙️ Setup

This project uses a SparkFun JetBot AI Kit V1. The [assembly guide](https://learn.sparkfun.com/tutorials/assembly-guide-for-sparkfun-jetbot-ai-kit/all) should be followed.

This project builds on the [Niantic Monodepth2 repository](https://github.com/nianticlabs/monodepth2) and the [NVIDIA Collision Avoidance](https://github.com/dusty-nv/jetson-inference). Cloning these are therefore necessary for full functionality. For the sake of valid references, the file structure described in the [file structure](###-📁-File-Structure).

The directory has a [requirements.txt](requirements.txt) file which can be used to install all necessary components. This is done in the terminal as such:
`$ pip3 install -r requirements.txt`
However, the Jetson Nano is extremely opposed to virtual environments and would not allow any version or any workaround. In addition to this, I only had access to one Jetbot. Therefore, the generated requirements file contained all modules of the Jetbot and jetson itself, and had to be trimmed manually. Therefore, this adds a possibility of human error in the conciseness and completeness of the [requirements.txt](requirements.txt) file. As a "devil or deep blue sea" workaround, there exists two requirements files: one untampered [requirementsComplete.txt](requirementsComplete.txt) to ensure completeness, and one trimmed [requirements.txt](requirements.txt) which is concise and most likely, but not guaranteed, covers all true requisite packages.
Therefore, either the concise requirements and complete requirements can be installed in the console/terminal in the respective ways:

`$ pip3 install -r requirements.txt`

or

`$ pip3 install -r requirementsComplete.txt`

### 📁 File Structure

The file structure used to complete the project is as follows:

```markdown
Directory
│
└───Hide 'n' Seek Project Directory
│ │ main.ipynb
│ │ main.py
│ │ Hide'n'Seek.ipynb
│ │ coco_labels.txt
│ │ best_model.pth
│ │ README.md
│ │
│ └───models
│ └───mono_640x192
│ .
| .
│ .
| .
│
└───monodepth2
│ .
│ .
│
└───jetson-inference
| .
│ .
│
└───jetbot
.
.
```

## 🔛 Startup

At startup, the Jetbot may need to log in. The standard password is "jetbot". When logged in, the Jetbot must be connected to the internet to serve its Jupyter server. As this is the only way to run the notebook remotely, we must connect to the internet. This can be done as one would with a normal computer, requiring most likely a mouse, a keyboard and a monitor. If the jetbot has previously been connected to the same network, reconnecting should happen automatically, requiring no extra components.

However, there is a bug where the Jetbot keeps activating and deactivating the search of a connection. The way to fix this is to restart the bot by pulling the cable from the Jetson Nano and reinserting it. If one were to restart the "proper" way through the menus, the Jetson Nano has a roughly 50% chance of using 30 minutes on updates it never accomplishes to finish. After this "reboot", it should connect automatically.

## ✅ Running

The program can be run as a Jupyter Notebook and as a python script. The Jupyter Notebook is orders of magnitude faster than the python file.

Before running, if the password of your Jetbot is not the standard "jetbot", the password variable must be changed in the few first lines in the code, where a call to the terminal is made to restart the nvargus-daemon.

### 🤖 Directly on JetBot

To run through the python script, all you need to do is enter the Hide 'n' Seek project directory, and run the main.py file:
`$ python3 main.py`.
This can be done directly from the Jetbot or through the terminal in the Jupyter server.

To run through the Jupyter Notebook, one would first have to enter the project repository and boot up Jupyter Notebook: `$ jupyter notebook`. From here we select the file we want: `main.ipynb`, a two-click run of the program for hands-off setup and running, and `Hide'n'Seek.ipynb`, an in-depth, sectionalized and structured implementation for more control.

### 🕹️ Remotely from Laptop (Recommended!)

To connect remotely to the JetBot through its Jupyter server, go to its ip-address displayed on its screen(SparkFun Micro OLED), through port 8888. E.g. if the ip displayed is 19.24.108.207, the one should go to [19.24.108.207:8888]().
From here, one should navigate into the project repository.

To run as a pure python script, one can open a terminal kernel and run `$ python3 main.py` This should start the script and the program runs.

To run through Jupyter, one can navigate to the file of choosing, either `main.ipynb` or `Hide'n'Seek.ipynb`. From there we can open it and start using it immediately by opening the file and using the "run" button.

### 🎆 Presentations

For presentations I would suggest using the two-step notebook `main.ipynb`. This way, one could run the setup cell and have the computationally heaviest segments already finished for when the program is to be demoed.

## ⏳ Further Training

The monodepth2 model is pretrained by nianticlabs and has not been altered. However, it is possible to train from scratch or fine-tune as laid out in [their documentation](https://github.com/nianticlabs/monodepth2#-training).
The Collision Avoidance model in [best_model.pth](best_model.pth) employs transfer learning on a pre-trained Alexnet. This has been done with use-case specific images to maximize performance in the lab where the program is to be used. Further fine-tuning is possible and encouraged for use in other locations than NAIL.
The object detection net is a SSD-MobileNet V2 model pre-trained on MS-COCO Data. I have not done any further training as the pre-trained net worked decently in use-case setting. However, further training is possible to allow for objects other than those in the dataset.

## ⭐️ Acknowledgements

- [nianticlabs](https://github.com/nianticlabs)
- [dustynv](https://github.com/dustynv)

## 🛠 Built With

- [Niantic Monodepth2 repository](https://github.com/nianticlabs/monodepth2)
- [NVIDIA Collision Avoidance and Object Following Examples](https://github.com/NVIDIA-AI-IOT/jetbot)

## 📝 Notes:

#### Shorthands used:

- OF: Object Following
- CA: Collision Avoidance
- OD: Object Detection
- MD: Monocular Depth Perception (Monodepth)

## ❌ Known Issues / fix

When the GPU gets overwhelmed with work, it tends to stop updating the camera values. This may perpetuate after the load is lightened and even after restarting the program and system. The only working fix I found was restarting the nvargus-daemon. This is done by running this line in the console: `$ sudo systemctl restart nvargus-daemon`. This must be done before instantiation the camera. To address this, the first lines of the code pushes a terminal command to

The Jetson Nano using the [Raspberry Pi NoIR Camera V2](https://www.raspberrypi.org/products/pi-noir-camera-v2/) is extremely near-sighted when it comes to object recognition. It accurately and notices objects within ~25cm. This applies for all feasible resolutions. This can be fixed by running on better hardware which can handle increased resolution.

## ❓ FAQ

#### **The display shows "no internet"**

Connect the Jetson to a monitor and check the internet connection from there.

#### **The Jetson will not connect to a known network within range**

Pull the power cable from the Jetson.

#### **The Jetson is using 45 minutes to shut down**

Do **NOT** pull the power cable from the Jetson while running the updates on shut down. These updates are never successfully installed and is why you shouldn't shut down the Jetson this way if you are in a time pinch.

#### **The JetBot program maintains the same motor functions constantly**

If the program pushes the same motor functions over a period, the camera has frozen. Stop the program by KeyboardInterrupt (or "Stop" through Jupyter), and restart. The nvargus-daemon restart at the start of the program should fix this problem.

#### **I want it to play against other objects than the default cup!**

One can edit the objects it will accept as players in the game by editing the contents of the variable "**accepted_classes**". If you want several objects to be recognized, the ID's must be added to the list seperated by the standard comma. i.e.
`accepted_classes = [47, 32, 19]`
The ID's are in _coco_labels.txt_ and is the number of the line it is in. The list is of course 0-indexed, meaning the object on line 1, has ID = 0. Hence, Car has ID = 3, person has ID = 1 and bus has ID = 6.

## ⏭ ToDo

The file structure is a mess. I got too deep into the web before I found that I would be the only one able to understand how it is connected, and now its been a month since I last looked at it and cannot remember a thing. Also, the file structure is too rigid. The sys.path is appended with the direct paths to the other modules. This should be changed to be relative, not explicit references.

For ease of use, I copied the mono_640x192 model into the Hide'n'Seek Project Directory. If references is updated to run through the `../monodepth2` package, it can be removed. Otherwise the monodepth2 package could be moved within the repository, with the corresponding references changed.

## ⚖️ License

This work has a standard MIT License, which can be found in [LICENSE.txt](LICENSE.txt)

## ⚠️ Disclaimer

This code was used in an educational manner, following the non-commercial license of Niantic Monodepth2.
