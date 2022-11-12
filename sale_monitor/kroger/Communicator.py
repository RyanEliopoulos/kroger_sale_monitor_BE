import os
import requests
from typing import Tuple


class Communicator:
    """
        Designed only for client credentials auth flow (not customer)
    """

    # App credentials
    client_id: str = os.getenv('sale_monitor_client_id')
    client_secret: str = os.getenv('sale_monitor_client_secret')
    # API urls
    api_base: str = 'https://api.kroger.com/v1/'
    token_endpoint: str = 'connect/oauth2/token'
    # Endpoint settings
    product_search_page_size = 15
    location_search_filter_limit = 50

    @staticmethod
    def get_clientcontext_token() -> Tuple[int, dict]:
        """ Hits the Kroger API token endpoint. Returns {'access_token': <access_token>} if successful
            I guess we'll just get a new token for every request.  Maybe not performant. Will consider some sort of
            caching mechanism.
        """
        # Staging HTTP request content
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
            , 'scope': 'product.compact'
        }
        target_url = Communicator.api_base + Communicator.token_endpoint
        req = requests.post(target_url, headers=headers, data=data, auth=(Communicator.client_id,
                                                                          Communicator.client_secret))
        if req.status_code != 200:
            print('Error retrieving Kroger tokens with client credentials..')
            print(req.status_code, req.text)
            return -1, {'error': req.text}
        return 0, req.json()  # keyed on access_token

    @staticmethod
    def search_products(search_string: str, location_id: str, page: int = 0) -> Tuple[int, dict]:
        """
            Hits the product search endpoint. Includes 'start' parameter, indicating how many products to skip
            in the search. Useful. We want this to support pagination for the sake of performance.
        :param search_string: Must be at least 3 characters
        :param page: Which slice of products to return.
        """
        print('In search_products')
        if len(search_string) < 3:
            return -1, {'error': 'search term must be at least 3 characters'}
        ret = Communicator.get_clientcontext_token()
        if ret[0]:
            print(f'Error in search_products: {ret}')
            return ret
        access_token: str = ret[1]['access_token']
        headers: dict = {
            'Accept': 'application/json'
            , 'Authorization': f'Bearer {access_token}'
        }
        filter_start = 1 + (page * Communicator.product_search_page_size)
        params = {
            'filter.term': search_string,
            'filter.locationId': location_id,
            'filter.fulfillment': 'csp',
            'filter.start': str(filter_start),
            'filter.limit': '15',
        }
        target_url: str = f'{Communicator.api_base}products'
        req = requests.get(target_url, headers=headers, params=params)
        if req.status_code != 200:
            print(f'Error in search_products: {req.text}')
            return -1, {'error': f'{req.status_code}: {req.text}'}
        print(f'Success in search_products: {req.json()}')
        return 0, {'results': req.json()}

    @staticmethod
    def product_details(upc: str, location_id: str) -> Tuple[int, dict]:
        print('in product_details')

        ret = Communicator.get_clientcontext_token()
        if ret[0]:
            print(f'Error in product_details: {ret}')
            return ret

        access_token = ret[1]['access_token']
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded'
            , 'Authorization': f'Bearer {access_token}'
        }
        params = {
            'filter.locationId': location_id
        }
        target_url: str = f'{Communicator.api_base}products/{upc}'

        req = requests.get(target_url, headers=headers, params=params)
        if req.status_code != 200:
            print(f'Error in product_details: {req.text}')
            return -1, {'error': req.text}
        print(f'Success in product_details: {req.json()}')
        return 0, {'response': req.json()}

    @staticmethod
    def search_locations(zipcode: str) -> Tuple[int, dict]:
        print('searching locations')
        ret = Communicator.get_clientcontext_token()
        if ret[0]:
            print(f'Error in search_locations: {ret}')
            return ret
        # Fresh tokens in hand
        access_token = ret[1]['access_token']
        # Building request
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        # Must be params. Call requests.get with these classed as 'data' failed the API call
        params = {
            'filter.zipCode.near': zipcode,
            'filter.limit': Communicator.location_search_filter_limit
        }
        target_url: str = Communicator.api_base + 'locations'
        req: requests.Response = requests.get(target_url, headers=headers, params=params)
        if req.status_code != 200:
            print(f'request error searching lcoations: {req.text}')
            return -1, {'error': f'{req.status_code}: {req.text}'}
        print(f'successfully searched locations: {req.json()}')
        return 0, {'results': req.json()}





