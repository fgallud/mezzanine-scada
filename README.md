# mezzanine-scada
It is an SCADA app that uses mezzanine as grafical user interface
- SVG pictures to design the schematic controls of the system
- the mezzanine WYSIWYG editor for designing the web interface
- A mathematical simulated hardware that allow to run a dummy system instead of the real one. This is a key feature in SCADA because the real systems can be dangerous, slow, and/or expensive to run


Detailed documentation is in the "docs" directory.

Install:

pip3 install git+https://github.com/fgallud/mezzanine-scada.git

Execute the example site:

cd /usr/local/lib/python3.6/dist-packages/mezzanine_scada

or the path your system installs python3 packages

cd example_projects/tank

python3 manage.py daemons start &
python3 manage.py runserer

and now you can see the example on your browser (I use mozzilla Firefox) on http://127.0.0.1:8000

Bear in mind that in the current state is useless



