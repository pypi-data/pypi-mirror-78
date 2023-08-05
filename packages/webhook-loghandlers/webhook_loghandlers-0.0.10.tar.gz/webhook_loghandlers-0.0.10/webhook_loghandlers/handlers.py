#!/usr/bin/env python3
import logging
import aiohttp
import asyncio
import warnings
from discord import Webhook, AsyncWebhookAdapter, Embed


class DiscordHandler(logging.Handler):
    '''
    Class for sending logs to discord webhooks
    '''

    _invalidURL: bool = False

    def __init__(self, url: str, secure: bool = False, embed: Embed = None) -> None:
        '''
        Set up a logging handler for Discord webhooks

        Parameters:
            url (str): URL of the Discord webhook

        Returns:
            None
        '''
        logging.Handler.__init__(self)

        self.url = url
        self.embed = embed
        self.__testConnection(url)

    def __testConnection(self, url: str) -> None:
        '''
        Test the connection to the webhook

        Parameters:
            url (str): URL of the webhook

        Returns:
            None
        '''
        r = requests.get(url)
        if r.status_code != 200:
            warnings.warn(f'Error establishing connection to webhook, URL returned a {r.status_code}')
            self._invalidURL = True
        return

    def mapLogRecord(self, record: logging.LogRecord) -> str :
        '''
        Map the logs to generate what the formatter specifies

        Parameters:
            record (logging.LogRecord): Log record to convert to specified formatting

        Returns:
            format(record) (str): Formatted log record
        '''
        return self.format(record)

    def emit(self, record: str) -> None:
        '''
        Send a log record to Discord

        Parameters:
            record (str): Log to be sent as a message to the discord webhook

        Returns:
            None
        '''
        if self._invalidURL:
            warnings.warm(f'Could not send log to webhook. URL is invalid')
            return
        self.__posthook(record)

    async def __postHook(self, record: str) -> None:
        '''
        Post the webhook asynchronously

        Parameters:
            record (str): Log message

        Returns:
            None
        '''
        try:
            url = self.url
            logMsg = self.mapLogRecord(record)
            headers = {'content-type': 'application/json'}
            logMsg = logMsg[:1900]
            data = json.dumps({'content': str(logMsg)})
            async with aiohttp.request('POST', url, data=data, headers=headers) as _:
                return
        except Exception:
            self.handleError(record)
