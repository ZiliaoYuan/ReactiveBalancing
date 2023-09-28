# SimSES_Python
Python Version of SimSES
SimSES (Simulation of stationary energy storage systems) is an open source modeling framework
 for simulating stationary energy storage systems. The tool, originally developed in MATLAB,
  was initiated by Maik Naumann and Nam Truong and is now transferred to Python and continuously
   improved by Daniel Kucevic and Marc Möller at the Institute for Electrical Energy Storage of the Technical University of Munich.

#### **Installation:**

The following packages need to be installed with version number if not the newest version is used:
- python 3.8
- scipy
- numpy
- pandas
- plotly
- matplotlib
- pytest
- pytz

There are several ways to install. It is recommended to use a virtual enviroment (Conda or Virtualenv).
- Graphically in Anaconda or Pycharm (see below)
- using pip commands (e.g. "_pip install numpy_")
- running the following command in the checked out repository with the correct eviroment selected:
_python setup.py install_

When you want to integrate a virtual enviroment into (or create one in) Pycharm go to:

_Settings/Project:SimSES_Python/Project Interpreter_

Click on the Settings icon in the top right and select add.
Depending which virtual enviroment you use select the corresponding option. 
Enter the path to the existing or new enviroment.
It should now show the used eviroment in the bottom right of the main window of Pycharm.
