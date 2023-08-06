#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import requests
from dli.client.components import SirenComponent
from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.models.account_model import AccountModel
from urllib.parse import urljoin


class Accounts(SirenComponent):

    def get_account_by_name(self, account_name):
        """
        Retrieves account details given an account name.

        :param str account_name: The name of the account. For example found
                                 on package tech data ops.

        :returns: account object
        """
        response = self.session.get(
            urljoin(
                self._environment.accounts,
                'api/identity/v2/dl_accounts'
            ),
            params={
                'filter[0][value]': account_name,
                'filter[0][operator]': 'eq',
                'filter[0][field]': 'name'
            }
        )

        response_data = response.json()

        if not response_data['data']:
            if not self.strict:
                self.logger.warning(
                    f'Account with name {account_name} not found')
                return None
            else:
                r = requests.Response()
                r.status_code = 404
                r.request = (lambda: True)
                r.request.method = f'Account with name {account_name} not found'
                r.request.url = ""
                raise CatalogueEntityNotFoundException(
                    message=f'Account with name {account_name} not found',
                    response=r
                )

        data = response_data['data'][0]

        return AccountModel._from_v2_response(data)
