from django import forms
from models import variable, channel

class variableForm(forms.ModelForm):
    CHANNEL_DIRECTION = (
        ('input','is a signal that is sampled'),
        ('output','is a signal that is generated'),
        ('dummy','is a signal without type'),
    )
    name = models.CharField('unique name of the variable', max_length=150)
    direction = models.CharField('direction of the variable',max_length=20,choices=CHANNEL_DIRECTION)
    name_gui = models.CharField('name of the variable user friendly', max_length=150,blank=True)
    description = models.TextField('descripcion', max_length=150,blank=True)
    origin = models.TextField('description of the hardware that generate/measure this variable', max_length=150,blank=True)
    destination = models.TextField('What is this variable for?', max_length=150,blank=True)


class channelForm(variableForm):
    nchannel = models.PositiveIntegerField()


