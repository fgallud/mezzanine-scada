The project is a standar mezzanine project but we need to do some changes:

in mysite/settings.py
add the base apps:

    "mezzanine_scada.base_theme",
    "mezzanine_scada.base",
    "mezzanine_scada.datalogging",
    "mezzanine_scada.hardware.simulated",
    "mezzanine_scada.control.state_machine",

at least base_theme needs to be near the top, adobe the standard mezzanine theme



in mysite/urls.py

add some urls in order to let javascript comunicate to python with ajax calls


#this code adds some urls to deal with ajax calls
from mezzanine_scada.base.views import validate_username
urlpatterns += [
    url('^ajax/validate_username/$', validate_username, name='validate_username'),
]








