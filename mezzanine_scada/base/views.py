from mezzanine_scada.base.models import scada_config
from django.http import JsonResponse
from xmlrpc.client import ServerProxy


server_port=scada_config.objects.first().server_port


def get_multiple_value(request):
#calls the get_multiple_value([name1, ...]) function by a xmlrpc call
#returns an array of dictionaries  {'value':valor, 'time':valor}
#    names = request.GET.get('names', None)
    names = request.GET.getlist('names[]')
    #
    #calls the database function.
    try:
        proxy = ServerProxy('http://localhost:%i' %server_port)
        data = proxy.get_multiple_value(names)
    except:
        data = {}
    return JsonResponse(data)

#we need to add to url.py the code to create the urls that ajax needs
#from mezzanine_scada.base.views import get_multiple_value
#urlpatterns += [
#    url('^ajax/get_multiple_value/$', get_multiple_value, name='get_multiple_value'),
#]



