"""This is the test module for main.app ."""

from google.appengine.ext import testbed
import pytest


# https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.testbed
testbed_instance = testbed.Testbed()
# Load testbed default env vars
testbed_instance.activate()
# Replaces testbed domain for local integration test with urllib2
# be sure to have you dev server running.
testbed_instance.setup_env(True, http_host='localhost:8080')
# Loads mail proxy stub
testbed_instance.init_mail_stub()


@pytest.fixture
def app():
    """App setup."""
    import main
    main.app.testing = True
    return main.app.test_client()


def test_match_example(app):
    """Test for the endpoint that matches tickets."""
    from app_config import cron_match_endpoint
    r = app.get(cron_match_endpoint)
    assert 'Notification sent to' in r.data.decode('utf-8')


def test_missing_example(app):
    """Test for the endpoint with missing tickets."""
    from app_config import cron_missing_endpoint
    r = app.get(cron_missing_endpoint)
    assert 'Missing match at' in r.data.decode('utf-8')
