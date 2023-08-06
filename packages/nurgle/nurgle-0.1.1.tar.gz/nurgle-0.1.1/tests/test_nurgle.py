#!/usr/bin/env python

"""Tests for `nurgle` package."""

import pytest


from nurgle.nurgle import Nurgle


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_constructor():
    nurgle = Nurgle(slack_token="", slack_channel="", state_file=".")
    nurgle = Nurgle()