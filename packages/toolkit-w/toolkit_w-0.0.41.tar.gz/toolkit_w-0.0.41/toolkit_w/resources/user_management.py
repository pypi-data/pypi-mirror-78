"""
Wisdom is the user interaction with Whatify wisdom, it contains

"""
# Prediction is the way to productize the Ensemble created in the previous steps. Once an Ensemble is created,
# users can upload additional Datasources that may be used for predictions.
#
# ‘Prediction’ API includes querying of predictions (Get, List and Delete) and creating a Prediction to get predictions
# on existing Ensembles and uploaded Datasources.
import os

import s3fs
from typing import Dict
import toolkit_w
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.errors import APIError
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class UserManagement(APIResource):
    _CLASS_PREFIX = ''

    @classmethod
    def list(cls, url: str='users/list', search_term: str = None, page: int = None, page_size: int = None, sort: Dict = None,
             filter_: Dict = None, api_key: str = None) -> WhatifyResponse:
        """
        List the existing Tasks - supports filtering, sorting and pagination.

        Args:
            search_term (Optional[str]): Return only records that contain the `search_term` in any field.
            page (Optional[int]): For pagination, which page to return.
            page_size (Optional[int]): For pagination, how many records will appear in a single page.
            sort (Optional[Dict[str, Union[str, int]]]): Dictionary of rules  to sort the results by.
            filter_ (Optional[Dict[str, Union[str, int]]]): Dictionary of rules to filter the results by.
            api_key (Optional[str]): Explicit `api_key`, not required, if `fireflyai.authenticate()` was run prior.
            :param url: the API url of users\accounts

        Returns:
            WhatifyResponse: users are represented as nested dictionaries under `hits`.
        """
        return cls._list(url=url, search_term=search_term, page=page, page_size=page_size, sort=sort, filter_=filter_, api_key=api_key)

    @classmethod
    def login(cls, email: str, password: str) -> WhatifyResponse:
        """
        Authenticates user and stores temporary token in `toolkit_w.token`.

        Other modules automatically detect if a token exists and use it, unless a user specifically provides a token
        for a specific request.
        The token is valid for a 24-hour period, after which this method needs to be called again in order to generate
        a new token.

        Args:
            email (str): email.
            password (str): Password.

        Returns:
            WhatifyResponse: Empty WhatifyResponse if successful, raises FireflyError otherwise.
        """
        url = 'login'

        requestor = APIRequestor()
        response = requestor.post(url, body={'username': email, 'password': password, 'tnc': None}, api_key="")
        toolkit_w.token = response['token']
        print(' '.join(['user mail:', str(email), '- Login successful']))

        return WhatifyResponse(status_code=response.status_code, headers=response.headers)

    @classmethod
    def impersonate(cls, user_id: str = None, email: str = None, admin_token: str = None) -> WhatifyResponse:
        """
       impersonate user and stores temporary token in `toolkit_w.token`

       Args:
           user_id (str): user ID.
           email (str): User email.
           admin_token (str): Admin user token.

       Returns:
           WhatifyResponse: Empty WhatifyResponse if successful, raises WhatifyError otherwise.
       """
        if email:
            user_id = None
            raise Exception('TODO: need tom implement get user ID from mail')

        url = ''.join(['users/login_as/', str(user_id)])
        requester = APIRequestor()
        response = requester.post(url, api_key=admin_token)
        toolkit_w.token = response['result']
        print(' '.join(['user ID:', str(user_id), '- Login successful']))
        return WhatifyResponse(status_code=response.status_code, headers=response.headers)

    @classmethod
    def get_user_list(cls, username: str, admin_token: str = None) -> WhatifyResponse:
        ret_val = {}
        resp = cls.list(filter_={'username': [username]}, api_key=admin_token)
        if resp and 'result' in resp and len(resp['result']) == 1:
            ret_val = resp['result'][0]
        return ret_val

    @classmethod
    def get_account_list(cls, name: str, admin_token: str = None) -> WhatifyResponse:
        ret_val = {}
        resp = cls.list(url='accounts', filter_={'name': [name]}, api_key=admin_token)
        if resp and 'result' in resp and len(resp['result']) == 1:
            ret_val = resp['result'][0]
        return ret_val

    # @classmethod
    # def test_API(cls, var_str: str, user_token: str = None) -> WhatifyResponse:
    #     print('aa' + str(var_str))
    #     # cls._list(search_term='auto_qa_admin')
    #     # url = ''.join(['users/login_as/', str(6206)])
    #     # url = ''.join(['accounts'])
    #     url = 'reports/predictions/25568/insights/summary'
    #     requester = APIRequestor()
    #     try:
    #         response = requester.get(url, api_key=user_token)
    #     except APIError as ex:
    #         print((str(ex)))
    #
    #     response = requester.post(url, api_key=user_token)
    #     print('sss')
    #     print('sss')
    #     print('sss')
    #     print('sss')

