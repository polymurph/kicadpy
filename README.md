# Kicad Scripts

Kicad Scripting toolbox

It is still in its infant state and will undergo many changes and restructuring until the first stable version.
It currently is built for **Kicad 7**.

---

## Table of Content

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Usage](#usage)
4. [FAQ](#faq)
5. [Contributing](#contributing)
6. [License](#license)
7.  [Contact](#contact)

---

## Usage

In this section different usecases are explained.

### Creating your own layout script an using it for a Kicad project

In this usecase the folderstruckture is following.
```
YourProjectName (root)
├── .git
└── YourKicadProjectFolder
    ├── file1.kicad_pcb
    ├── file2.sch
    ├── file3.pro
    └── file4.lib
```

Please note that if you dont use git it is stil possible to use this explanation. Just step over the steps related with git.

KicadPy is intended to be used as a git submodule.
Befor following the following steps please add and commit all previouse git work.

This s done by going inside the  ```YourKicadProjectFolder``` and run the command.

```
git submodule add https://github.com/polymurph/KiCadPy.git
```

Then go back into the root folder and add the KiCadPy to git by runing the following commands

```
git add .gitmodules, KiCadPy
git commit -m "added KiCadPy as submodule"
```

TODO: explain how to setup up the script, use KiCadPy inside the script and call the script from the scripting console from Kicadpy.

---

## FAQ

### Questions related to Kicad

#### How to remove silkscreen from footprint

[link](https://maskset.net/kicad-pcbnew-scripting-removing-ref-des-from-silk-screen.html)

#### How to execute a script?


```exec(open('<file name>.py').read())```

#### How to install Python modules for Kicad Scripting?

[Reddid source](https://www.reddit.com/r/KiCad/comments/unl7s1/how_to_install_python_packages_for_kicad_scripting/)


For Windows go to the folder where Kicad program files are places on your system. In the designated folder open the command promt. There you can run ```pip install <module name>```

#### How to create custom DRC rules

Inside the PCB editor go to the board setup and there go under Design Rules to Custom rules. There open up the Syntax help and copy the entire content and paste it inside chatGPT. then thell Chat gpt to create e.g a clearance rule between the net class A and B of 5 mm fo all entitys. Copy paste the output of chatGPT into the DRC rules window.
This way of creating rules must be further investigatet for new methods and possibilities.

### Questions related to Python

#### How to create a Python library

[How to create a Python library by Kia Eisinga](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f)

---

## Ideas

https://jeffmcbride.net/kicad-track-layout/

---

## Sources
https://docs.kicad.org/doxygen-python-7.0/index.html

[KiCad Developer Documentation](https://dev-docs.kicad.org/en/)
