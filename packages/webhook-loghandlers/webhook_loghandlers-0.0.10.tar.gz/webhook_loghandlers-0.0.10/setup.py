#!/usr/bin/env python3
from setuptools import setup

setup(
    name = "webhook_loghandlers",
    version = "0.0.10",
    description = "Handlers for the logging module to send logs to discord/slack webhooks",
    url = "https://github.com/MEhrn00/webhook-loghandlers",
    author = "Matt Ehrnschwender",
    author_email = "matthewe2020@gmail.com",
    packages = ["webhook_loghandlers"],
    install_requires = [
        "requests",
        "aiohttp",
        "asyncio"
    ],
    classifiers = [
        "Programming Language :: Python :: 3"
    ],
)
