LogglyHipChatHeroku
===================

A small service to forward Loggly alerts to HipChat. Doesn't require any configuration of the app or any credentials, all parameters are simply entered in the URL of the Loggly config screen like any other HipChat integration.


## Basic Setup ##
1. Fork or clone the repo to get a local copy
2. Install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and login.
3. Run `heroku create` from the root directory of the repo. It will create a url like hungry-hippo1234.herokuapp.com. This is {YourUrl} used in the next step.
4. In the Loggly 'Alert Endpoints' section, create a new endpoint of type 'HTTP Endpoint' and set the URL to {YourUrl}?auth_token={HipChatAuthToken}&room_id={HipChatRoom}. Set the method to POST and make sure to use HTTPS for the URL.


## Advanced ##

**Optional HipChat parameters**

Other Hipchat parameters can be specified in the Loggly Alert url and they will be passed onto the Hipchat API.
e.g. 
`https://hungry-hippo1234.herokuapp.com?room_id=543432&auth_token=73b298e62f927ac9273&color=red&from=MyService&notify=true`

**Modifying the message template**

The file `message_template.html` is a template that can be modified. All of the loggly data fields are top level properties of the template data. Any hipchat parameters are under .hipchat and any other parameters passed in via query string are available at .custom. Template docs here: http://www.tornadoweb.org/en/branch4.0/template.html

**Custom parameters**

Any parameters passed via the query string that are not supported by the HipChat message api will be passed into the template under the key of 'custom'.
e.g. In the Loggly Endpoint setup add `&arbitrary_name=some_value` and then tn the template `Got a log entry from {{ custom['arbitrary_name'] }}.`

**Fields included in the Loggly webhook post body**

```Javascript
{
    edit_alert_link : "https://{account}.loggly.com/alerts/edit/1234",
    source_group : "N/A",
    start_time : "Oct 23 19:07:01",
    end_time : "Oct 23 19:12:01",
    search_link : "https://{account}.loggly.com/search/?terms=tag%3A%22some-tag%22&source_group=&savedsearchid=12345&from=2014-10-23T19%3A07%3A01Z&until=2014-10-23T19%3A12%3A01Z",
    query : "tag:\"some-tag\" ",
    num_hits : 48,
    owner_username : "{username}",
    owner_subdomain : "{account}",
    owner_email : "somebody@example.com",
    recent_hits : [
        "{\"level\":\"INFO\",\"time\":\"2014-10-23T19:11:10.8526140+00:00\",\"message\":\"Something is happening.\"}"
    ]
}
```

The 'recent_hits' are individually deserialized before being passed into the template.