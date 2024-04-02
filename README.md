# Color Segmentation Toolbox - can be used to segment colored Tumor cells

This project contains Python scripts to run a streamlit application "ColorSegmentationToolbox" in your browser. It offers a browser based GUI to segment Hue colors with different Saturations in images.

# Installation instructions

1. If you do not already have Anaconda or Miniconda installed, download and install Anaconda for your operating system (use the default install options):

	https://www.anaconda.com/download

2. Open an Anaconda-Prompt on your system. (Click Start, search for Anaconda Prompt, and click to open.) On Linux or Mac open a terminal window.

3. Navigate to the downloaded files in the Anaconda-Prompt (terminal) window. If you do not know how to change folders in a Command-Pompt (with "cd"- Command), google it :-). 

4. In the same folder where the file "requirements.txt" is, run this command in the Anaconda-Prompt:

```shell
conda create --name ColorSegmentationToolbox -y
```

This should create a python enviroment with the name "ColorSegmentationToolbox" 


5. Activate the new environment by typing into the same Anaconda-Prompt window:

```shell
conda activate ColorSegmentationToolbox
```

6. Install all needed python packages into the new python enviroment by:

```shell
conda install --file requirements.txt -y
```
	
7. Now launch the streamlit application from the terminal in the same folder as above:

```shell
python -m streamlit run Segmentation.py
```

Your default browser should open the application on your local machine. It should look like this: 
![Screenshot](https://github.com/RBartho/ColorSegmentationToolbox/tree/main/images/toolbox_screenshot.png)
The browser is only used as an interface. No data is uploaded to the Internet.

# Starting the application (after installation)

1. On MacOS and Linux open a terminal, on Windows open a Anaconda Prompt. Navigate to the downloaded folder containing the Segmentation.py file.

2. Activate the created Python environment by typing into the terminal
```shell
conda activate ColorSegmentationToolbox
```
3. Now start the application with:

```shell
python -m streamlit run Segmentation.py
 ```

# Notes on using the application

1. If you want to restart the app, just refresh your browser. All loaded data will be removed and all active calculations will stop.

2. If you want to close the app, just close the tab in your browser and the terminal or Anaconda Prompt.

3. While computations are running do not interact with the application (e.g. selecting SIPs, Sidebar, uploading or deleting images) This would refresh the application and all progress will be lost.

4. Multithreading is not supported as it would limit platform independence. To speed up calculations, you may want to consider splitting the data and running multiple instances of the application.

5. The number of images you can load into the application at one time is limited by your hard-drive. Also note, large images require much more processing time than smaller images.

# Privacy and security
All calculations and data transfers of the application take place on your local computer. The browser is only used as an interface. No data is uploaded to the Internet.

# Contributers
Ralf Bartho: Toolbox concept, code development, maintenance, bugfixes 
Hanna Maar: Toolbox concept, beta testing
