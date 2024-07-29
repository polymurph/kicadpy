# Getting Started with kicadpy

## Setup

The following steps will show you how to set up kicadpy.

Clone the repository in a directory of your choice

``` Bash
cd ~
git clone https://github.com/polymurph/kicadpy 
```
    
Copy the absolute directory path of the newly cloned kicadpy repo.

Find the ```PyShell_pcbnew_startup.py``` file inside the Kicad application
directory.

> [!TIP]
>     For Windows the ```PyShell_pcbnew_startup.py``` file is normally located under ```~\AppData\Roaming\kicad\8.0```.
>     For Linux it is under```~/.config/kicad/8.0/PyShell_pcbnew_startup.py```.

Open it up and insert the following code snippet.

``` python
import sys
# the absolute file path to the kicadpy repo
kicadpy_dir = '~/AbsPathTo/kicadpy/'
sys.path.append(kicadpy_dir)
import kicadpy as kp
sys.path.append(kp.getProjectPath())
```

Replace ```~/AbsPathTo/kicadpy/``` with the prevoius copied absolute path to
kicadpy.

This code will append the kicadpy to the system paths at startup of the Kicad Console. It creates a link sothat kicadpy is callable.

Now lets test the implementation by opening up the kicad project and opening
up the layout. Inside the layout editor open the console. In the output test
you should see the message ```Info: Kicadpy is ready to be used``` pop up.

----

# How to use

## interactive Scripting inside the kicad console

TODO: explain how its done. Give some examples with pictures etc.

## Creating a script for the layout

Let's say you want to create a script which places 10 vias in a
circular pattern around a given center point. The following steps will show you how this can be done.
This example uses the following file structure as a demonstration.

```
YourProjectName (root)
├── .git
└── YourKicadProjectFolder
    ├── file1.kicad_pcb
    ├── file2.sch
    ├── file3.pro
    └── file4.lib
```

Create a python file inside the folder ```YourKicadProjectFolder``` . In this
case we name it ```layoutScript.py```. Your folder structure should look as
shown below.

```
YourProjectName (root)
├── .git
└── YourKicadProjectFolder
    ├── file1.kicad_pcb
    ├── file2.sch
    ├── file3.pro
    ├── file4.lib
    └── layoutScript.py
    ```

This file will contain the python script for your layout.

Open the file ```layoutScript.py``` and add the following code snippet.

```python
import kicadpy as kp

kp.via.placeCircularArray(
    0,      # centerX_mm
    0,      # centerY_mm
    10,     # radius_mm
    0.2,    # drillDiameter_mm
    0.5,    # width_mm
    0,      # startAngle_DEG
    360,    # endAngle_DEG
    1)      # n_vias

kp.layoutRefresh()
```

Save and close the file.

Now open up the layout and open up the console. Inside the console execute the
script as followed.

```python
exec(open(r"AbsolutePathTo\YourProjectName\YourKicadProjectFolder\layoutScript.py").read())
```

After execution the layout should look like this.

<img src="./resources/ViaCircularArrayExample.jpg" width="300" height="auto">

---
