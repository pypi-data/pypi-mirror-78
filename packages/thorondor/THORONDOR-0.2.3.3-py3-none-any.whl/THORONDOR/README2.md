# Presentation of THORONDOR, a program for data analysis and treatment in NEXAFS

Authors : Simonne and Martini

#### The Program is meant to be imported as a python package, if you download it, please save the THORONDOR folder in ...\Anaconda3\Lib\site-packages
There are two main classes in THORONDOR to use:

### The class Spectrum
A new instance of the spectrum class will be initialized for each spectrum saved in the data folder. This object is then saved in the list "ClassList", attribute of the second class "GUI".
For each spectrum, all the different dataframes that will be created as well as specific information e.g. $E_0$ the edge jump can be find as attributes of this class. Certain attributes are instanced directly with the class, such as:
* Name of spectrum
* Path of original dataset
* Timestamp

At the end of the data reduction, each spectrum should have at least three different data sets as attributes, saved as `pandas.DataFrame()`:
* df : Original data
* ShiftedDf : If one shifts the energy 
* ReducedDf : If one applies some background reduction or normalization method 
* ReducedDfAthena : If one applied the specific Athena background reduction and normalization method.

A Logbook entry might also be associated, under `Spectrum.LogbookEntry`

It is possible to add commentaries for each spectrum by using the `Spectrum.Comment()` and to specify some additional inf with the function `Spectrum.AdditionalInfo()`.

Each Spectrum can be retrieved by using the function Spectrum.unpickle() with the path of the saved Class as an argument.

### The class GUI
This  class is a Graphical User Interface (GUI) that is meant to be used to process important amount of XAS datasets, that focus on similar energy range (same nb of points) and absorption edge.
There are two ways of initializing the procedure in a jupyter notebook:
* `GUI = THORONDOR.GUI()`; one will have to write the name of the data folder in which all his raw datasets are saved, in a .txt format.
* `GUI = THORONDOR.GUI.GetClassList(DataFolder = "<yourdatafolder>")` ;if one has already worked on a folder and wishes to retrieve his work.

This class makes extensive use of the ipywidgets and is thus meant to be used with a jupyter notebook. Additional informations are provided in the "ReadMe" tab of the GUI.

All the different attributes of this class can also be exported in a single hdf5 file using the pandas .to_hdf5 methods. They should be accessed using the read_hdf methods from pandas.

The necessary Python packages are : numpy, pandas, matplotlib, glob, errno, os, shutil, ipywidgets, IPython, scipy, datetime, importlib, pickle, lmfit and inspect.

### FlowChart

![FlowChart](https://user-images.githubusercontent.com/51970962/76894984-6e65d180-688f-11ea-9649-cee5aad148ce.png)

### Screenshots of the program

![GUIShowData](https://user-images.githubusercontent.com/51970962/74930247-768c3780-53dd-11ea-9403-111a2fbd3a6d.png)

![GUIReadme](https://user-images.githubusercontent.com/51970962/74930045-1d240880-53dd-11ea-9271-aa2efbee7a3c.png)

![GUILogbook](https://user-images.githubusercontent.com/51970962/74930291-8a379e00-53dd-11ea-8aae-803c227f33f1.png)

![GUIPlot](https://user-images.githubusercontent.com/51970962/74930304-90c61580-53dd-11ea-85b7-467dfd054e06.png)

![GUIReduce](https://user-images.githubusercontent.com/51970962/74930315-97ed2380-53dd-11ea-96fb-6dbb6938ea83.png)

![GUIShift](https://user-images.githubusercontent.com/51970962/74930326-9f143180-53dd-11ea-8ab3-0c7817b8af6d.png)

![GUIFit](https://user-images.githubusercontent.com/51970962/76788429-32f9d300-67bb-11ea-8402-a734634fd3f3.PNG)


### For users on Jupyter Lab, please follow this thread : https://stackoverflow.com/questions/49542417/how-to-get-ipywidgets-working-in-jupyter-lab

### Improvements yet to be made:
	check if all the time complexity are opti
    Use more  ternary operators
	underscore for numbers, f strings
	more zip and enumerate
	underscore values is unused, unpack with *c
    use setattr and getattr
    platypus op