import os
import sys

def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

setup_environment()

from appmodels.models import *

mapping = { "Deluxe" : "D",
            "Night Service" : "N",
            "Express" : "X",
            "AC Volvo" : "AC",
            "M-Service" : "M",
            "Limited Stop" : "LSS",
            "Ordinary" : "O",
            "Limited Stop Night Service" : "LSS N",
            "Express Night Service" : "X N",
            "Point to Point" : "LSS",
            "M Service" : "M",
            "M-Service Night Service" : "M N",
            "" : "O"}

def cleanup_type(type):
    return type.replace("Cut Service", "").replace("Extension", "").replace("Not Figured Out Yet","").strip()

distRoutes = Route.objects.values("display_name").distinct().order_by('display_name')

for dR in distRoutes:
    r = Route.objects.filter(display_name = dR['display_name'])[0]
    sameR = Route.objects.filter(display_name=r.display_name)
    types = [mapping[cleanup_type(sR.types)] for sR in sameR]
    ntypes = []
    for t in types:
        if not t in ntypes:
            ntypes.append(t)
    r.types = ','.join(ntypes)
    Route.objects.filter(display_name=r.display_name).exclude(id=r.id).delete()
    r.save()
    print r.display_name
#   print sameR
