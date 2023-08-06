#!/usr/bin/env python3
"""Returns the email(s) that can be used to verify an SSL for a site

 domain -- domain to request email info on
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
"""

from .com_error import errorProcess
from .sendRequest import ApiCredentials, ApiUrl, makeRequest

api_creds = ApiCredentials()
api_endpoint = ApiUrl.api_endpoint

def getDomainApproverEmail(domain):
    url = api_endpoint+'prov/v1/domain/emails'
    try:
        assert domain is not None
        payload = {
            'api_id': api_creds.api_id,
            'api_key': api_creds.api_key,
            'domain': domain
        }
        r = makeRequest(url, payload)
        r.rase_for_status()
        return r.text
    except AssertionError as error:
        return errorProcess(error, domain)
    except Exception as error:
        return errorProcess(error)