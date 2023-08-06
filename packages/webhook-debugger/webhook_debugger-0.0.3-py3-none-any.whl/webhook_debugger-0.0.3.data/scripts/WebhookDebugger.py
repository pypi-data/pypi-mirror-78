#!python
import http.server
import ssl
import argparse
import http.client

version = "0.0.3"

results=None
enable_forward=False

def debug(msg):
    if results.stdout:
        print(msg)

class WebhookDebug(http.server.BaseHTTPRequestHandler):

    def compose(self,method,url,header,body,ip=None):
        msg="["+method+"]:\n"
        if results.show_url:
            msg += str(url)+"\n"
        if results.show_header:
            msg += "[HEADERS]:\n"+str(header)+"\n"
        if results.show_body:
            msg += "[BODY]:\n"+str(body)+"\n"
        if results.show_ip:
            msg += "[Client IP]:\n"+str(ip[0])+"\n"
        return(msg)


    def compose_forward(self,header,body):
        msg="\n[Response]:\n"
        if results.forward_show_header:
            msg += "[HEADERS]:\n"+str(header)+"\n"
        if results.forward_show_body:
            msg += "[BODY]:\n"+str(body)+"\n"
        return(msg)


    def simpleResponse(self,Response):
        self.wfile.write(str(Response).encode(encoding='utf_8', errors='strict'))


    def forward(self,method,headers,path,forward_url,forward_port,use_ssl,body=None):
        conn = None
        if use_ssl:
            conn = http.client.HTTPSConnection(forward_url,forward_port)
        else:
            conn = http.client.HTTPConnection(forward_url,forward_port)
        headers.replace_header("Host",forward_url +":"+ str(forward_port))
        conn.request(method,path,headers=headers,body=body)
        print(headers)
        response = conn.getresponse()
        self.send_response(response.status)
        for key in response.getheaders():
            self.send_header(*key)
        self.end_headers()
        data = response.read()
        print(response.getheaders())
        self.wfile.write(data)
        return(data,response.getheaders())


    def do_HEAD(self,Content_type="text/plain",status=200):
        self.send_response(status)
        self.send_header("Content-type", Content_type)
        self.end_headers()


    def do_GET(self):
        self.server_version = results.server_version
        self.sys_version = results.sys_version
        get_data="No GET Body"
        try:
            content_length = int(self.headers['Content-Length'])
            get_data = self.rfile.read(content_length)
        except:
            pass
        if enable_forward:
            data, headers = self.forward("GET",self.headers,self.path,results.forward_url,results.forward_port,results.forward_ssl)
            if results.show_get and (results.ip == None or self.client_address[0] in results.ip):
                debug(self.compose("GET",self.path,self.headers,get_data,self.client_address) + self.compose_forward(headers,data))
            return
        else:
            self.do_HEAD(results.content_type,results.status)
        if results.show_get and (results.ip == None or self.client_address[0] in results.ip):
            response = self.compose("GET",self.path,self.headers,get_data,self.client_address)
            if results.response == None:
                self.simpleResponse(response)
            else:
                self.simpleResponse(results.response)
            debug(response)


    def do_POST(self):
        self.server_version = results.server_version
        self.sys_version = results.sys_version
        post_data = None
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
        except:
            pass
        if enable_forward:
            data, headers = self.forward("POST",self.headers,self.path,results.forward_url,results.forward_port,results.forward_ssl,body=post_data)
            if results.show_post and (results.ip == None or self.client_address[0] in results.ip):
                debug(self.compose("POST",self.path,self.headers,post_data,self.client_address) + self.compose_forward(headers,data))
            return
        else:
            self.do_HEAD(results.content_type,results.status)
        if results.show_post and (results.ip == None or self.client_address[0] in results.ip):
            response = self.compose("POST",self.path,self.headers,post_data,self.client_address)
            if results.response == None:
                self.simpleResponse(response)
            else:
                self.simpleResponse(results.response)
            debug(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='WebhookDebugger', description='Debug Webhooks')
    parser.add_argument('-p', '--port', action='store', type=int, dest='port', default=8080, help='set server Port default=8080')
    parser.add_argument('-a', '--addr', action='store', dest='addr', default="0.0.0.0", help='set server address default 0.0.0.0')
    parser.add_argument('--no-stdout', action='store_false', dest='stdout', default=True, help='disable log to stdout')
    parser.add_argument('-s', '--status', action='store', type=int, dest='status', default=200, help='set Http Status Code default=200 disabled by forward')
    parser.add_argument('-c', '--content-type', action='store', dest='content_type', default="text/plain", help='set Content-Type default=text/plain disabled by forward')
    parser.add_argument('--no-header', action='store_false', dest='show_header', default=True, help='disables Header output')
    parser.add_argument('--no-body', action='store_false', dest='show_body', default=True, help='disables Body output')
    parser.add_argument('--no-url', action='store_false', dest='show_url', default=True, help='disables Url output')
    parser.add_argument('--no-ip', action='store_false', dest='show_ip', default=True, help='disables IP output')
    parser.add_argument('-r', '--response', action='store', dest='response',default=None, help='define response default same output as STDOUT disabled by forward')
    parser.add_argument('--no-post', action='store_false', dest='show_post', default=True, help='disables POST output')
    parser.add_argument('--no-get', action='store_false', dest='show_get', default=True, help='disables GET output')
    parser.add_argument('--ip', action='store', dest='ip', default=None, help='shows only the output for the given ips spaerator=,')
    parser.add_argument('--ssl-cert', action='store', dest='sslcert', default=None, help='path to ssl cert (LEs fullchain.pem)')
    parser.add_argument('--ssl-key', action='store', dest='sslkey', default=None, help='path to ssl key (LEs privkey.pem)')
    parser.add_argument('--server-version', action='store', dest='server_version', default='WebhookDebugger/'+version, help='set Server Version default=WebhookDebugger/'+version)
    parser.add_argument('--sys-version', action='store', dest='sys_version', default='WebhookDebugger/python', help='set Sys Version default=WebhookDebugger/python')
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)
    sub = parser.add_subparsers(help='additional help',title='subcommand',dest='forward')#'action='store',dest='enable_forward'
    forward = sub.add_parser('forward')
    forward.add_argument('--url', action='store', dest='forward_url', default=None, help='set Back-ends URL',required=True)
    forward.add_argument('--port', action='store', dest='forward_port', default=None, help='set Port Back-end is listeing on',required=True)
    forward.add_argument('--no-stdout', action='store_false', dest='forward_stdout', default=True, help='disable log to stdout')
    forward.add_argument('--use-ssl', action='store_true', dest='forward_ssl', default=False, help='disables forwarding using SSL')
    forward.add_argument('--no-header', action='store_false', dest='forward_show_header', default=True, help='disables Header output')
    forward.add_argument('--no-body', action='store_false', dest='forward_show_body', default=True, help='disables Body output')
    forward.add_argument('--no-url', action='store_false', dest='forward_show_url', default=True, help='disables Url output')
    results = parser.parse_args()
    if results.forward:
        enable_forward = True
    if results.ip != None:
        if "," in results.ip:
            results.ip = results.ip.split(",")
        else:
            results.ip = [results.ip]
    try:
        server = http.server.HTTPServer((results.addr, results.port), WebhookDebug)
        server.server_version = results.server_version
        server.sys_version = results.sys_version
        print('Started http server ' + results.addr + ':' + str(results.port))
        if results.sslcert != None and results.sslkey != None:
            try:
                server.socket = ssl.wrap_socket (server.socket, certfile=results.sslcert, keyfile=results.sslkey, server_side=True) #ssl_version=results.protocol
            except:
                print("Error setting up SSL")
                exit(1)
            print("SSL enabled")
        else:
            if results.sslcert != None and results.sslkey != None:
                print("SSL disabled")
        server.serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
        server.socket.close()
