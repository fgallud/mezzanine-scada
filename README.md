# mezzanine-scada
It is an SCADA app that uses mezzanine as grafical user interface
- SVG pictures to design the schematic controls of the system
- the mezzanine WYSIWYG editor for designing the web interface
- A mathematical simulated hardware that allow to run a dummy system instead of the real one. This is a key feature in SCADA because the real systems can be dangerous, slow, and/or expensive to run


Detailed documentation is in the "docs" directory.

Install:

Linux:
sudo pip3 install mezzanine

sudo pip3 install git+https://github.com/fgallud/mezzanine-scada.git

Windows :
pip3 install mezzanine

pip3 install git+https://github.com/fgallud/mezzanine-scada.git

clone this project:
git clone https://github.com/fgallud/mezzanine-scada

Execute the example site:
Linux:
cd mezzanine-scada/mezzanine_scada/example_projects/tank
Windows:
cd mezzanine-scada\mezzanine_scada\example_projects\tank

Linux:
sudo python3 manage.py daemons start &
sudo python3 manage.py runserver
Windows:
python3 manage.py daemons start &
python3 manage.py runserver


and now you can see the example on your browser (I use mozzilla Firefox) on http://127.0.0.1:8000

the user is admin and the password is admin

Bear in mind that in the current state is useless



