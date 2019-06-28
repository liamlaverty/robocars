# robocars
Using genetic programming to teach cars to drive a flash game.

This project uses the gaming_assembly.py file to genetically train cars to go around a given racing track. With enough training these cars should be able to navigate any new track given to them. The library pyparticles.py is used to keep all the code relating to the cars and the environment (and their interactions) separate.

Requires pygame, pickle, PIL(/Pillow), numpy.



****

## Getting Started

For a quick getting started guide if you've got no experience with python:

* Clone or download the project from [Simon's github profile](https://github.com/drsimonclark/robocars) (green button on the right hand side & click "download zip", save it on your computer and extract)

### I do not have VSCode and/or python installed:

* Download and install [Visual Studio Code](https://code.visualstudio.com/) (VSCode)
* Download and install [Python](https://www.python.org/downloads/) (v3.7.3 works)
* Open VSCode and click the Extensions pane in the left hand toolbar. Search for [Python for Visual Studio Code (also available here)](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* VSCode may suggest some extensions in the bottom right hand corner. They're optional ease-of-use features
* Continue to the next section

### I have VSCode and Python installed:

* Open the project in VSCode by going to `File -> Open Folder` and opening the folder you have the project saved in
* Click `Terminal -> New Terminal`
* Run the following commands (these will take some time to install. The following code will install several python applications onto your computer):
  - `py -m pip install -U pygame --user`
  - `py -m pip install -U numpy --user`
  - `py -m pip install -U image --user`
  - `py -m pip install -U pickle --user`
* Open the file explorer in the left hand toolbar and select the file `gaming_assembly.py`
* press `f5` on your keyboard to launch the game
* Select `current python file`
* To exit the generation, press `Shift F5`

***
