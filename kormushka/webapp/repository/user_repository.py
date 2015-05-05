from loginsys.models import CustomUser

def getAllUsers():
    return CustomUser.objects.filter()

def getUsersByDeparts(departs_pks):
    return CustomUser.objects.filter(po__depart__in=departs_pks)