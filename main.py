import os
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template
from tornado.escape import json_encode, json_decode
import hipchat

logging.getLogger().setLevel(logging.INFO)
logging.info('Starting Up')

hipchat_parameter_names = ['room_id','from','color','notify','auth_token']
 
class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
    def get(self):
        self.write(json_encode({'status': 'OK'}))
        
    def post(self):
        hipchat_params = self._get_hipchat_query_params()
        hipchat_params['from'] = hipchat_params.get('from','Loggly')
        
        template_data = json_decode(self.request.body);
        template_data['hipchat'] = hipchat_params;
        template_data['custom'] = self._get_custom_query_params()
        template_data['recent_hits'] = self._decode_recent_hits(template_data['recent_hits'])
        
        hipchat_params['message'] = self._create_message_text(template_data);
  
        self._send_hipchat_message(hipchat_params);
  
        self.write(json_encode({'result': 'sent'}))
        
    def _send_hipchat_message(self, hipchat_params):
        hipster = hipchat.HipChat(token=hipchat_params['auth_token'])
        hipster.method('rooms/message', method='POST', parameters=hipchat_params)
        logging.info('Sent HipChat message')
        
    def _create_message_text(self, template_data):
        with open('message_template.html','r') as f: template = f.read()
        compiled_template = tornado.template.Template(template)
        
        message_text = compiled_template.generate(**template_data)
        logging.debug('Message text is "' + message_text + '"')
        
        return message_text
        
    def _get_hipchat_query_params(self):
         return {
            k: self.get_query_argument(k) 
            for k in hipchat_parameter_names 
            if self.get_query_argument(k, None) != None }
            
    def _get_custom_query_params(self):
        all_arg_names = [k for k in self.request.query_arguments.keys() if k not in hipchat_parameter_names]
        return {k:self.get_query_argument(k) for k in all_arg_names}
        
    def _decode_recent_hits(self, hits):
        return [x for x in self._decode_json_generator(hits)]
    
    def _decode_json_generator(self, hits):
        for hit in hits:
            escaped = self._escape_json_control_characters(hit)
            logging.debug('Decoding hit: "' + escaped + '"')
            try:
                yield json_decode(escaped)
            except ValueError as error:
                logging.exception(error)
    
    def _escape_json_control_characters(self, input_str):
        return input_str.replace('\\','\\\\').replace('\r\n', '\\r\\n')
 
 
def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()