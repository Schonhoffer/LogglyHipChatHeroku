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

The file `message_template.html` is a template that can be modified. All of the loggly data fields are top level properties of the template data. Any hipchat parameters are under .hipchat and any other parameters passed in via query string are available at .custom.