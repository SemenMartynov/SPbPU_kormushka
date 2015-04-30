import sys

try:
    from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC, ALL_ATTRIBUTES, SUBTREE
    from ldap3.core.exceptions import LDAPInvalidCredentialsResult, LDAPPasswordIsMandatoryError
except ImportError:
    pass


from django.utils import timezone
from loginsys.models import CustomUser
from django.contrib.auth.models import User
from webapp.models import Depart, PO
from django.contrib.auth.backends import ModelBackend
from kormushka.settings import AUTH_INFORMATION

import logging
logger = logging.getLogger(__name__)

LDAP_INFORMATION = AUTH_INFORMATION['LDAP']

class LdapSynchronizer():

    def __init__(self, *args, **kwargs):
        self.ldap_server = Server(LDAP_INFORMATION['HOST'], port=LDAP_INFORMATION['PORT'])


    def sync(self):



        c = Connection(self.ldap_server,
                       authentication=AUTH_SIMPLE,
                       client_strategy=STRATEGY_SYNC,
                       raise_exceptions=True)
        c.open()

        if c.search(search_base=LDAP_INFORMATION["GROUPS_DN"], search_filter = '(objectClass=posixGroup)', search_scope=SUBTREE, attributes=ALL_ATTRIBUTES):
            departs_information = c.response
            logger.warn(departs_information)
            for depart_information in departs_information:
                depart_id = depart_information["attributes"]['gidnumber'][0]
                depart_name = depart_information["attributes"]['cn'][0]
                try:
                    depart = Depart.objects.get(pk__exact=depart_id)
                    depart.name = depart_name
                    depart.depart = 0
                    depart.save()
                    logger.warn("({}) update depart.".format(depart_name))
                except Depart.DoesNotExist:
                    depart = Depart()
                    depart.id = depart_id
                    depart.name = depart_name
                    depart.depart = 0
                    depart.save()
                    logger.warn("({}) create depart".format(depart_name))
                usergroup_search_filter =  LDAP_INFORMATION["USERGROUP_SEARCH_FILTER"].format(depart_id)  # Example: '(uid={})'
                if c.search(search_base=LDAP_INFORMATION["BASE_DN"], search_filter=usergroup_search_filter, search_scope=SUBTREE, attributes=ALL_ATTRIBUTES):
                    users_information = c.response
                    now = timezone.now()
                    for user_information in users_information:
                        exact_username = user_information['attributes']["uid"][0]
                        first_name = " ".join(user_information['attributes']["givenName"])
                        last_name = " ".join(user_information["attributes"]["sn"])
                        email = ""
                        if hasattr(user_information['attributes'], "mail"):
                            email = user_information['attributes']['mail'][0]
                        try:
                            user = CustomUser.objects.get(username__exact=exact_username)
                            # always update proteus user profile to synchronize ldap server
                            user.first_name = first_name
                            user.last_name = last_name
                            user.email = email
                            user.last_login = now
                            user.save()
                            logger.warn("({}) logged in.".format(exact_username))
                            try:
                                _depart=Depart.objects.get(id=depart_id)
                                _user=CustomUser.objects.get(id=user.id)
                                logger.warn("dep_id: {}".format(_depart))
                                logger.warn("us_id: {}".format(_user))
                                po = PO.objects.get(depart=_depart, user=_user)
                            except PO.DoesNotExist:
                                _depart=Depart.objects.get(id=depart_id)
                                _user=CustomUser.objects.get(id=user.id)
                                po = PO()
                                po.depart = _depart
                                po.user = _user
                                po.save()
                                logger.warn("({}) logged in - initial".format(exact_username))
                        except User.DoesNotExist:
                            user = CustomUser()
                            user.username = exact_username
                            user.first_name = first_name
                            user.last_name = last_name
                            user.email = email
                            user.is_staff = True
                            user.is_superuser = True
                            user.is_active = True
                            user.last_login = now
                            user.save()
                            logger.warn("({}) logged in - initial".format(exact_username))
                            try:
                                _depart=Depart.objects.get(id=depart_id)
                                _user=CustomUser.objects.get(id=user.id)
                                logger.warn("dep_id: {}".format(_depart))
                                logger.warn("us_id: {}".format(_user))
                                po = PO.objects.get(depart=_depart, user=_user)
                            except PO.DoesNotExist:
                                _depart=Depart.objects.get(id=depart_id)
                                _user=CustomUser.objects.get(id=user.id)
                                po = PO()
                                po.depart = _depart
                                po.user = _user
                                po.save()
                                logger.warn("({}) logged in - initial".format(exact_username))


        return "false"