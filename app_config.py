"""Simple config file."""

import os


# https://console.cloud.google.com/appengine/settings?project=[PROJECT_ID]&serviceId=default
email_api_authorized_sender = 'your.good.self@example.com'

cron_match_endpoint = '/cron_match_endpoint'

cron_missing_endpoint = '/cron_missing_endpoint'

example_url = 'http://{}/example.html'.format(os.environ['HTTP_HOST'])
