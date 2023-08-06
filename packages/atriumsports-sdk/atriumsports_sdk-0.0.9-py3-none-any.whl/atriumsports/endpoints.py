""" A file defining all the endpoint addresses """

def get_endpoints(environment, url_type):
    """ return urls for the atriumsports environments """
    envs = {
        'auth': {
            'production': 'https://token.prod.cloud.atriumsports.com/v1/oauth2/rest/token',
            'nonprod': 'https://token.nonprod.cloud.atriumsports.com/v1/oauth2/rest/token',
            'sandpit': 'https://token.sandpit.cloud.atriumsports.com/v1/oauth2/rest/token',
            'localhost': 'http://localhost:XXXX',
        },
        'api': {
            'production': 'https://api.dc.prod.cloud.atriumsports.com',
            'nonprod': 'https://api.dc.nonprod.cloud.atriumsports.com',
            'sandpit': 'https://api.dc.sandpit.cloud.atriumsports.com',
            'localhost': 'http://localhost:XXXX',
        },
        'streamauth': {
            'production': 'https://token.prod.cloud.atriumsports.com/v1/stream/XXXX/access',
            'nonprod': 'https://token.nonprod.cloud.atriumsports.com/v1/stream/XXXX/access',
            'sandpit': 'https://token.sandpit.cloud.atriumsports.com/v1/stream/XXXX/access',
            'localhost': 'http://localhost:XXXX',
        },
    }
    if not envs.get(url_type):
        return None
    url = envs[url_type].get(environment) or ''
    return url
