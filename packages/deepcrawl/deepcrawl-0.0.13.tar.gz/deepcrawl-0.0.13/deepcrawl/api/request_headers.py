from deepcrawl.exceptions import InvalidContentType


# Generate request headers with the API connection token and the appropriate content-type
def get_request_headers(token="", content_type='json'):
    headers = {
        'X-Auth-Token': token,
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate'
    }

    if content_type == 'json':
        headers.update({"Content-Type": 'application/json'})
    elif content_type == 'form':
        headers.update({"Content-Type": 'application/x-www-form-urlencoded'})
    elif not content_type:
        pass
    else:
        raise InvalidContentType

    return headers
