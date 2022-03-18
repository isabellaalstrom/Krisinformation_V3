import json
import httpx
import logging

from .exceptions import *
from .const import VERSION, DOMAIN, USER_AGENT, BASE_URL, NEWS_PARAMETER, VMAS_PARAMETER

logger = logging.getLogger(DOMAIN)


class kriscom(object):
    def __init__(self, timeout=None):
        self._timeout = timeout

    def version(self):
        return VERSION

    async def requestVmas(self):

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BASE_URL + VMAS_PARAMETER,
                    headers={"User-agent": USER_AGENT},
                    # allow_redirects=True,
                    timeout=self._timeout,
                )
        except Exception as e:
            error = HTTP_Error(997, f"A HTTP error occured: {str(e)}", str(e))
            logger.debug(error)
            raise error

        try:
            response.encoding = "UTF-8"
            intermediateResponse = json.dumps(response.json())
            jsonResponse = json.loads(intermediateResponse)
        except Exception as e:
            error = API_Error(995, f"A parsing error occured: {str(e)}", str(e))
            logger.debug(error)
            raise error

        return jsonResponse

    async def requestNews(self):

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    BASE_URL + NEWS_PARAMETER,
                    headers={"User-agent": USER_AGENT},
                    # allow_redirects=True,
                    timeout=self._timeout,
                )
        except Exception as e:
            error = HTTP_Error(997, f"A HTTP error occured: {str(e)}", str(e))
            logger.debug(error)
            raise error

        try:
            response.encoding = "UTF-8"
            intermediateResponse = json.dumps(response.json())
            jsonResponse = json.loads(intermediateResponse)
        except Exception as e:
            error = API_Error(995, f"A parsing error occured: {str(e)}", str(e))
            logger.debug(error)
            raise error

        return jsonResponse