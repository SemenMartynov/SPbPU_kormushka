from webapp.models import Depart

def getAllDeparts():
    return Depart.objects.filter()