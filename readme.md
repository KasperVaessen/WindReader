# WindReader
This application was developed for the Wind Tunnel in the "PWS Lab" from the TU Delft. It should be adoptable for similar projects using Phidget.

## Setting the project
Make sure to have the [Phidghet22](https://www.phidgets.com/docs/Main_Page) drivers installed.

To make sure the software works as it supposed to, please use a Virtual Environment.

Go to the root of the project directory and setup a virtual environment. This project was developed in Python 3.9.13. It should also work on other versions, but I have not tested this.

```bash
python -m venv venv
```

Activate the virtual environment.

```bash
call venv\Scripts\activate
```

Install the dependencies using the package manager [pip](https://pip.pypa.io/en/stable/). This should be done inside the virtual environment.

```bash
pip install -r requirements.txt
```

## Running the python project
Run the application inside the virtual environment
```bash
python src/main_application.py
```

## Creating with Qt (designer)
The GUI of WindReader has been created with PySide6 (A version of PyQT available under the LGPL license.). To edit the GUI follow these steps.

Run the following command in the virtual environment.
```bash
pyside6-designer
```

This will open the designer application of Qt. Here you can open the ui file located in `ui/main.ui`. 

In the editor you can edit the GUI however you want. Save the file after you are done.

To convert the gui to a python file the application can interact with, run the following command.

```bash
pyside6-uic ui/main.ui -o src/priv/mainwindow.py
```

**Please do not edit the mainwindow.py file directly** 
This file will be overwritten when the previous command is executed again. Instead edit it via `main_application.py`.

## export to executable with pyinstaller
To compile the application to an executable which can directly be distributed without the user installing python, pyinstaller is used. To prevent windows from detecting the application as a trojan, please follow the following steps (You only have to do this once).

### Create python bootloader

Make sure you are in the virtual environment.

Clone the [pyinstaller repository](https://github.com/pyinstaller/pyinstaller/)
```bash
git clone https://github.com/pyinstaller/pyinstaller.git
```

Go to the root of the repository you just cloned and go the bootloader folder.

```bash
cd bootloader
```

Make the bootloader.

```bash
python ./waf all
```
return back to the root of the repository.

Add the new version of pyinstaller to pip.

```bash
pip install .
```

### Create executable
```bash
pyinstaller src/main_application.py -n WindReader -w -i resources/icon.ico
```

This will create an executable in the folder `dist/WindReader`.

## Create windows installer with Inno Setup

Finally, for windows users, a installer can be created. For this you can use [Inno Setup](https://jrsoftware.org/isinfo.php). The process speaks for itself. Do make sure you include the `dist/WindReader/_internal/` folder when it asks for other application files.