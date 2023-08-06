from pymasmovil.client import Client
from pymasmovil.errors.exceptions import AccountRequiredParamsError


class Account():
    _route = '/v0/accounts'

    town = ""
    surname = ""
    stair = ""
    roadType = ""
    roadNumber = ""
    roadName = ""
    region = ""
    province = ""
    postalCode = ""
    phone = ""
    name = ""
    id = ""
    flat = ""
    email = ""
    door = ""
    documentType = ""
    documentNumber = ""
    corporateName = ""
    buildingPortal = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(Account, key):
                setattr(self, key, value)

    @classmethod
    def get(cls, session, account_id):
        """
        Returns a account instance obtained by id.

        :param id:
        :return: Account:
        """

        account_response = Client(session).get(
            route='{}/{}'.format(cls._route, account_id))

        return Account(**account_response)

    @classmethod
    def create(cls, session, **new_account):
        """
            Creates an account instance.

            :param **new_account:
            :return:
        """

        required_paramether_list = ['documentNumber', 'documentType', 'email',
                                    'phone', 'postalCode', 'province', 'region', 'roadName',
                                    'roadNumber', 'roadType', 'town']

        if 'documentType' not in new_account:
            raise AccountRequiredParamsError('documentType')

        if new_account['documentType'] == "CIF":
            required_paramether_list.append("corporateName")
        else:
            required_paramether_list.extend(["name", "surname", "nationality"])

        for required_paramether in required_paramether_list:
            if required_paramether not in new_account:
                raise AccountRequiredParamsError(required_paramether)

        new_account_id = Client(session).post(cls._route, (), new_account)

        return Account(id=new_account_id, **new_account)
