
## Perimeter, a Blender addon for QOL Titanfall 2 modding



code is a mess rn, will sort it out sometimes in the future.

FOR NOW DO NOT USE THE RPAK EXPORTER OR MATERIALOVERRIDES IF YOU ARENT SURE WHAT YOU ARE DOING, THEY ARE MESSED UP AND IM WORKING ON A NEW CENTRALIZED MATERIAL SYSTEM


## Setup


In Blender install Blender Source Tools addon, if you dont have it this wont work https://developer.valvesoftware.com/wiki/Blender_Source_Tools
Download the addon as a zip using the cool green button up there.

Install the addon in blender, enable it, and in its settings select your titanfall 2 folder, press the "setup studiomdl" button and select either your source film maker, portal 2(with sdk)or alien swarm (with sdk) install folders.

Somewhere on your pc make a folder and put repak.exe https://github.com/r-ex/RePak in there
put texconv.exe https://github.com/microsoft/DirectXTex/releases/download/jun2023/texconv.exe
and mdlshit.exe https://github.com/headassbtw/mdlshit/releases/download/2.3.2/mdlshit_windows_x64.zip
in there too, select them in the addons preferences

# how to use:

FOR IMORTED MODELS PLEASE WHEN DECOMPILING IN CROWBAR CHECK THE "REMOVE PATH FROM MATERIAL FILE NAMES"

While it works it still has alot of things to make better/fix, so for now please consider the following:
    
    Do not use the "setup empty rpak shader" on the same material twice. will add reset button in the future.

    dont use material overrides if you arent completely sure on how to make then work, they are wonky. 


its intended to be used for the final export part, as its way of handling some things are specific, for help consult the images below or contact me on discord ```4v_```

These 3 images should explain it a bit. 


![perimeter_panel](https://github.com/EM4Volts/Perimeter/blob/main/docs/perimeter_panel.jpg?raw=true)
![materials_panel](https://github.com/EM4Volts/Perimeter/blob/main/docs/materials_panel.jpg?raw=true)
![qc_panel](https://github.com/EM4Volts/Perimeter/blob/main/docs/qc_panel.jpg?raw=true)

## Issues / Bugs

Make an issue in the cool issues section up there, or if you fixed them make a PR and ill look at it in about 20 years.
## License

[GPL3](https://github.com/EM4Volts/Perimeter/blob/main/LICENSE)


