# Kicad Scripts
Kicad Scripting toolbox

## How to Script in Kicad?

supports currently Kicad 7


## Questions

### How to remove silkscreen from footprint

[link](https://maskset.net/kicad-pcbnew-scripting-removing-ref-des-from-silk-screen.html)

### How to execute a script?


```exec(open('<file name>.py').read())```

### How to install Python modules for Kicad Scripting?

[Reddid source](https://www.reddit.com/r/KiCad/comments/unl7s1/how_to_install_python_packages_for_kicad_scripting/)


For Windows go to the folder where Kicad program files are places on your system. In the designated folder open the command promt. There you can run ```pip install <module name>```

### How to create custom DRC rules
Inside the PCB editor go to the board setup and there go under Design Rules to Custom rules. There open up the Syntax help and copy the entire content and paste it inside chatGPT. then thell Chat gpt to create e.g a clearance rule between the net class A and B of 5 mm fo all entitys. Copy paste the output of chatGPT into the DRC rules window.
This way of creating rules must be further investigatet for new methods and possibilities.


## Ideas

https://jeffmcbride.net/kicad-track-layout/

## Sources
https://docs.kicad.org/doxygen-python-7.0/index.html

[KiCad Developer Documentation](https://dev-docs.kicad.org/en/)

