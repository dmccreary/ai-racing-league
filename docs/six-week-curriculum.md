# Sample Six-Week Curriculum

This is a sample suggested curriculum for a six week AI Racing League summer school project.  The students would all meet together for two hours, once a week.  There are then homework assignments. The students don't need any prior experience.

## Week 1: Overview and Unboxing

1. Slides: Welcome to the AI Racing League? [Link to Slides](slides/Welcome-to-the-ARL.pptx)
2. What is the DonkeyCar?
3. Lab: Unbox the car (requires tools such as cable tie cutter and screwdrivers)
4. What is AI? What is Machine Learning?
5. What is Python?
6. [Introduction to Python](https://www.coderdojotc.org/python/trinket/00-introduction/) course
7. Motors and servos (demo of car driving with the motors and servos being controlled by RC)
8. Make sure students know how to turn on the ESC and listen for the startup beep sound

See the suggested parts list for week 1

## Week 2: Booting a Raspberry Pi, UNIX, Calibration, Intro to Python and Raspberry Pi

1. Booting a Raspberry Pi from Micro SD card
   1. What is a Raspberry Pi?
   2. How much RAM do we need?
   3. Why is 4GB important for the AI Racing League?
   4. What is a micro SD card?  How big a card do we need? 32GB vs 65GB vs 128GB
   5. Can we train our model on a Pi?  Training vs. Inference - when do we need a GPU?
   6. What is an Operating System Image file?
   7. How do we create an image file?
   8. Download a Raspberry Pi image [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
   9. Burn a microSD card with that image - include customization
   10. Use the microSD card to boot your Raspberry Pi (requires 4GB Raspberry Pi Pico, keyboard, mouse, power supply, monitor)
2. Configure Pi desktop - learn how to use menus, add bookmarks to the web browser, manage bookmarks
5. Start Python IDE
6. Run "hello world" in Python
7. Open a Terminal and type "ls"
8. Download the DonkeyCar software
8. Get familiar with the folder layout
9. Verify the connections from the Pi to the PWM card and the DonkeyCar
9. Run the calibration command, write down the numbers for throttle and steering

## Week 3: Python, Configuration, Drive

1. More Python labs - get as far as possible through the [Introduction to Python](https://www.coderdojotc.org/python/trinket/00-introduction/) class
2. Get familiar with the Donkey Car configuration file
3. Focus on the key parameters for calibration
4. Find the Drive command
5. Discuss options for controlling the car: Joystick vs Web Application
6. Backup Career Exploration: What is a Software Engineer?
5. Backup Lab: [Google Teachable Machines](https://teachablemachine.withgoogle.com/)

## Week 4: Gather Image Data and Analyze Quality with Jupyter Notebooks

1. Drive around the track and gather image data
2. Look at the image data in the tubs
3. Run a basic Python program to count the number of files
4. Learn about a Jupyter Notebook
5. Backup Career Exploration: What is a Data Scientist?

## Week 5: The GPU and Training

1. Learn about the GPU - what are GPU cores? - Why is training time faster?
2. What is a conda environment for Python?
2. What is Miniconda [Download here](https://docs.conda.io/en/latest/miniconda.html)
3. Activating conda environments
4. Verifying that the GPU setting are correct
5. Run a test program on the GPU
6. Learn how to transfer files from the car's memory to the GPU (compress tubs, copy to jump drive)
7. What is a model file?  How big is your model?  What are model parameters?
8. Backup: What is Bias in AI?  How to we detect it?  How dow we measure it?

## Week 6: Using the Model to Drive Autonomously

1. Put the model file on the Donkey car
2. Run the drive with model command
3. Change the configuration files
4. Evaluate image quality