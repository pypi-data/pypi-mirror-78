import json
import requests
from .key import get_key, reset_key


def trigger_api(ppl_or_org, since_time=None,
                sort_order=None, page=1,
                name=None, query=None, domain_name=None,
                locations=None, types=None, socials=None):
    # Basic inputs.
    headers = {'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
               'x-rapidapi-key': get_key()}
    url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-"

    # Organization.
    if ppl_or_org:
        querystring = {"updated_since": str(since_time),
                       "sort_order": sort_order, "page": page, "name": name,
                       "query": query, "domain_name": domain_name,
                       "locations": locations, "organization_types": types}
        url += "organizations"
    # People.
    else:
        querystring = {"updated_since": str(since_time),
                       "sort_order": sort_order, "page": page, "name": name,
                       "query": query, "socials": socials,
                       "locations": locations, "types": types}
        url += "people"

    while True:
        # Request visit.
        response = requests.request("GET", url, headers=headers,
                                    params=querystring)

        # Success.
        if 200 == response.status_code:
            return json.loads(response.text)
        else:
            # Wrong key: re-enter the key.
            if 500 == response.status_code:
                headers['x-rapidapi-key'] = reset_key()
            # Other failures: raise an error.
            else:
                response.raise_for_status()
