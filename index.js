var express = require('express')
var bodyParser = require('body-parser');
var app = express();

app.set('port', (process.env.PORT || 5000))

app.use(bodyParser.json({ type: 'text/plain*' }))

var recorded_requests = [];

app.get('/', function(request, response) {
  response.json(recorded_requests);
});

app.post('/', function(request, response) {
  var request_details = {
      body: request.body,
      params: request.params,
      query: request.query
  };
  recorded_requests.push(request_details);
  response.json(request_details);
});


app.listen(app.get('port'), function() {
  console.log("logglyHipChatHeroku app is running on port:" + app.get('port'))
})