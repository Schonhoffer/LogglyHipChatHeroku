var express = require('express')
var bodyParser = require('body-parser');
var hipchat = require('node-hipchat');
var _ = require('underscore');
var Handlebars = require('handlebars');
var fs = require('fs');

var app = express();
app.set('port', (process.env.PORT || 5000));
app.use(bodyParser.json({ type: ['text','json'] }));

var compiled_message_template = getMessageTemplate('message_template.hbs');
var hipchat_parameter_names = ['room','from','color','notify','auth_token'];

app.get('/', function(request, response) {
  response.json({status: 'OK'});
});

app.post('/', function(request, response) {
  var hipchat_params = _.pick(request.query, hipchat_parameter_names);
  hipchat_params.from = hipchat_params.from || 'Loggly';
  
  var template_data = request.body;
  template_data.hipchat = hipchat_params;
  template_data.custom = _.omit(request.query, hipchat_parameter_names);
  
  hipchat_params.message = createMessage(template_data);
  
  sendHipChat(hipchat_params);
  
  response.json({result: 'sent'});
});

function createMessage(template_data){
    return compiled_message_template(template_data);
}

function sendHipChat(params){
    var HC = new hipchat(params.auth_token);

    HC.postMessage(params, function(data) {
        console.log('Sent HipChat message');
    });
}

function getMessageTemplate(file_name){
    var source = fs.readFileSync(file_name, {encoding: 'utf8'});
    return Handlebars.compile(source);
}

app.listen(app.get('port'), function() {
  console.log('LogglyHipChatHeroku app is running on port:' + app.get('port'));
})