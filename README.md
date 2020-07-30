# NAIL-Jetson-Demo-Project

NAIL-Jetson-Demo-Project is a Python project in relation to my summer internship at the Norwegian AI Lab (NAIL) at NTNU.
This project is made to work on the SparkFun JetBot AI Kit, with the final product being a showcase of different AI tools in a relatable setting to spark interest in the attendees. 
My approach was to emulate and win a game of [Hide and Seek](https://en.wikipedia.org/wiki/Hide-and-seek) against inanimate objects, within the [COCO dataset](https://cocodataset.org/).
This was achieved using a hierarchical combination of Monocular Depth Estimation, Object Detection and Collision Avoidance, having Object Detection override on the other two, 
Collision Avoidance on Monocular Depth Estimation, and Monocular Depth Estimation always running until told otherwise.
