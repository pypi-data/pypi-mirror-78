import requests
from pensionpro.errors import *

class ContactAPI(object):
    def __init__(self, api):
        self._api = api
    
    def get_contact(self, contact_id, **kwargs):
        """Fetches the contact for the given contact ID"""
        url = f'contacts/{contact_id}'
        contact = self._api._get(url, **kwargs)
        return contact
    
class PlanAPI(object):
    def __init__(self, api):
        self._api = api

    def get_plan(self, plan_id, **kwargs):
        """Fetches the plan for the given plan ID"""
        url = f'plans/{plan_id}'
        plan = self._api._get(url, **kwargs)
        return plan
    
    def list_plans(self, **kwargs):
        """Returns a list of all plan contact roles that match the filter"""
        url = f'plans'

        if 'skip' not in kwargs:
            kwargs['skip'] = 0

        if 'top' not in kwargs:
            kwargs['top'] = 1000

        plans = []
        has_next_page = True

        while has_next_page:
            this_page = self._api._get(url, **kwargs)
            plans += this_page["Values"]
            has_next_page = this_page["HasNextPage"]
            kwargs['skip'] += kwargs['top']
        
        return plans

class PlanContactRoleAPI(object):
    def __init__(self, api):
        self._api = api
    
    def get_plan_contact_role(self, plan_contact_role_id, **kwargs):
        """Fetches the plan contact role for the given plan contact role ID
            NOTE: A PlanContactRole is the association between a plan and a contact. This is NOT the role type!
        """
        url = f'plancontactroles/{plan_contact_role_id}'
        plan_contact_role = self._api._get(url, **kwargs)
        return plan_contact_role

    def list_plan_contact_roles(self, **kwargs):
        """Returns a list of all plan contact roles that match the filter"""
        url = f'plancontactroles'

        if 'skip' not in kwargs:
            kwargs['skip'] = 0

        if 'top' not in kwargs:
            kwargs['top'] = 1000

        plan_contact_roles = []
        has_next_page = True

        while has_next_page:
            this_page = self._api._get(url, **kwargs)
            plan_contact_roles += this_page["Values"]
            has_next_page = this_page["HasNextPage"]
            kwargs['skip'] += kwargs['top']
        
        return plan_contact_roles

class API(object):
    def __init__(self, username, api_key):
        """Creates a wrapper to perform API actions.

        Arguments:
            username: PensionPro username
            api_key: API Key
        """

        self._session = requests.Session()
        self._session.headers = {'accept': 'application/json', 'username': username, 'apikey': api_key}
        self._api_prefix = 'https://api.pensionpro.com/v1/'

        self.contacts = ContactAPI(self)
        self.plans = PlanAPI(self)
        self.plan_contact_roles = PlanContactRoleAPI(self)
    
    def _action(self, r):
        try:
            j = r.json()
        except ValueError:
            j = {}
        
        error_message = 'PensionPro Request Failed'
        if "errors" in j:
            error_message = f'{j.get("description")}: {j.get("errors")}'
        elif "message" in j:
            error_message = j["message"]

        if r.status_code == 400:
            raise PensionProBadRequest(error_message)
        elif r.status_code == 401:
            raise PensionProUnauthorized(error_message)
        elif r.status_code == 403:
            raise PensionProAccessDenied(error_message)
        elif r.status_code == 404:
            raise PensionProNotFound(error_message)
        elif r.status_code == 429:
            raise PensionProRateLimited(
                f'429 Rate Limit Exceeded: API rate-limit has been reached untill {r.headers.get("x-retry-after-seconds")} seconds.'
            )
        elif 500 < r.status_code < 600:
            raise PensionProServerError(f'{r.status_code}: Server Error')
        
        # Catch other errors
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise PensionProError(f'{e}: {j}')

        # Return json object
        return j

    def _get(self, url, **kwargs):
        """Wrapper around request.get() to use API prefix. Returns the JSON response."""
        args=[]
        for k,v in kwargs.items():
            args.append(f'${k}={v}')
        args = '&'.join(args)

        complete_url = f'{self._api_prefix}{url}?{args}'

        request = self._session.get(complete_url)
        return self._action(request)