# appengine-notificator
App Engine Cron tasks notifications tutorial.

In this project we use App Engine's Python Standard Environment to setup a Cron task in order to parse a website using BeautifulSoup, looking for specific keywords and notifying you by email when there's match.

Here are some detailed instructions on how to get you started if you've never deployed an App Engine project before:

1. Go to https://console.developers.google.com and  click **Create project** with your YOUR_PROJECT_ID.

2. Then go to https://console.cloud.google.com/appengine/start?project=YOUR_PROJECT_ID and:
  * Review the **App Engine Docs** section: [Download Google App Engine SDK](https://cloud.google.com/appengine/docs?hl=en_US) and [Browse docs](https://cloud.google.com/appengine/downloads?hl=en_US)

  * Then on **Your first app** section select **Python** as a language.

3. On the next screen select your location preference and wait while Google is *Preparing your App Engine services*.

4. After that follow the **App Engine Quickstart** tutorial on the right side of the screen to get familiar with the service.

  ![alt text](http://i.imgur.com/X8vaKFD.gif)

5. Now let's get down to the nitty-gritty and `git clone` this repo on your local dev directory.

6. Get the **Version** id from the code deployed on the tutorial, we'll need it later to keep things simple: https://console.cloud.google.com/appengine/versions?project=YOUR_PROJECT_ID&serviceId=default

7. Follow these instructions to get your dev environment set up (read the Hombrew caveats note below just in case): https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/README.md

8. Verify that you can run this app on your local directory:
```
$ dev_appserver.py app.yaml
```

9. Visit `http://localhost:8080` and follow the Cron endpoints example links. When seeing the "Not logged in" prompt just click Login, this is because our Cron endpoints will require admin login privileges.

10. If the previous links are working, change the value of `email_api_authorized_sender` on the file `app_config.py` to your admin email address.

11. Authorize your admin email by adding it to the Email API authorized senders field in the Settings section on App Engine: https://console.cloud.google.com/appengine/settings?project=YOUR_PROJECT_ID&serviceId=default

12. Now deploy the app executing the following command on your local directory (use the Version id you got on step 6.):
```
$ appcfg.py update -A PROJECT_ID app.yaml -V VERSION_ID
```

13. It's time to test the project on the Internet: https://PROJECT_ID.appspot.com/

14. If you got the email while testing the endpoints on appspot, you can now uncomment the lines at `cron.yaml` if you want to see the task running on prod. Deploy the Cron with the following command:
```
$ gcloud app deploy cron.yaml
```

15. You can see the deployed Crons and even trigger them manually here: https://console.cloud.google.com/appengine/taskqueues/cron?project=PROJECT_ID&serviceId=default&tab=CRON

16. Here's more info on App Engine's Cron configuration: https://cloud.google.com/appengine/docs/standard/python/config/cron

17. Don't forget to redeploy `cron.yaml` commenting out the lines like before so you don't spam yourself :) Enjoy creating your own notifications!


### Hombrew for macOS caveats

To save you a headache if you get a [**DistutilsOptionError** error](http://stackoverflow.com/questions/4495120/combine-user-with-prefix-error-with-setup-py-install) when running `pip install ...` run following commands:

```
$ printf "[install]\nprefix=" > $HOME/.pydistutils.cfg
$ pip install -t lib -r requirements.txt
$ rm $HOME/.pydistutils.cfg
```
