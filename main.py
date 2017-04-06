# -*- coding: utf-8 -*-
"""This is the main.app module."""

from bs4 import BeautifulSoup
from app_config import cron_match_endpoint
from app_config import cron_missing_endpoint
from app_config import email_api_authorized_sender
from app_config import example_url
from flask import Flask
from google.appengine.api import app_identity
from google.appengine.api import mail
import os
import urllib2


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def main():
    """Display the cron example endpoints and dev cron jobs links."""
    response = """<h3>Example Cron Endpoints</h3>
<p><a href="{}">Match endpoint</a></p>
<p><a href="{}">Missing endpoint</a></p>
<hr>""".format(cron_match_endpoint, cron_missing_endpoint)

    # Link to App Engine's local development Cron Jobs
    if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        response += '<a href="http://localhost:8000/cron">Dev Cron Jobs</a>'

    return response


@app.route(cron_match_endpoint)
def match_example():
    """Cron example endpoint that matches tickets."""
    match = __match_tickets(example_url, 'Final', '09/04/17')
    return handle_match(match, example_url)


@app.route(cron_missing_endpoint)
def missing_example():
    """Cron example endpoint with missing tickets."""
    match = __match_tickets(example_url, 'Missing', '20/20/20')
    return handle_match(match, example_url)


def handle_match(match, url):
    """Should there be a match, format a message and send a notification."""
    if match:
        message = "Match found at {}:\n{}".format(url, match)
        return __send_notification(url, message)
    else:
        return 'Missing match at: {}'.format(url)


def __match_tickets(url, name, date):
    html_doc = urllib2.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Match by CSS selector
    for el_row in soup.select('div.searchList tr'):
        el_name = el_row.select('td.event')
        el_date = el_row.select('td.date')

        # Extract text from matched elements
        if len(el_name) and len(el_date):
            t_name = el_name[0].get_text()
            t_date = el_date[0].get_text()

            # Find matching substrings
            if t_name.find(name) > -1 and t_date.find(date) > -1:
                return '{} - {}'.format(t_name, t_date)
    return None


# https://cloud.google.com/appengine/docs/standard/python/mail/sending-mail-with-mail-api
def __send_notification(source_url, message):
    app_id = app_identity.get_application_id()

    mail.send_mail(sender=email_api_authorized_sender,
                   to=email_api_authorized_sender,
                   subject='{} notification'.format(app_id),
                   body=message)

    return 'Notification sent to: {}'.format(email_api_authorized_sender)
