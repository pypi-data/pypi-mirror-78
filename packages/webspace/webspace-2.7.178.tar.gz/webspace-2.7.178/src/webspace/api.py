import json
import requests
import logging

logger = logging.getLogger('api')


class API:
    api_root = 'https://api.snoweb.fr'

    @staticmethod
    def request(path, data, method='post'):
        res = requests.request(
            url='%s%s' % (API.api_root, path),
            method=method,
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
            }
        )
        if res.status_code != 200:
            logger.error('Error API')
            logger.error(str(res.content))
            return None
        logger.debug('Request API OK')
        return res.content
