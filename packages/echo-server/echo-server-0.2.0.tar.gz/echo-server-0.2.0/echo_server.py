import os
import time
import click
import threading
try:
    from socketserver import BaseRequestHandler
    from socketserver import ThreadingMixIn
    from socketserver import TCPServer
    from socketserver import UDPServer
except ImportError:
    from SocketServer import BaseRequestHandler
    from SocketServer import ThreadingMixIn
    from SocketServer import TCPServer

BUFFER_SIZE = 1024

class ThreadedTCPRequestHandler(BaseRequestHandler):

    def handle(self):
        print("CLIENT CONNECTED: ", self.request)
        while True:
            data = self.request.recv(BUFFER_SIZE)
            print(self.request, data)
            if not data:
                break
            else:
                self.request.send(data)
        print("CLIENT SHUTDOWN: ", self.request)

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass

@click.command()
@click.option("-i", "--ignore-failed-ports", is_flag=True)
@click.option("-b", "--binding", default="0.0.0.0", help="Default to 0.0.0.0.")
@click.argument("port", nargs=-1)
def run(ignore_failed_ports, binding, port):
    """Start echo server on given ports. Press CTRL+C to stop.
    The default listenning port is 3682. You can listen on many ports at the same time.

    Example:

    echo-server 8001 8002 8003
    """
    ports = port
    if not ports:
        ports = [3682]
    servers = []
    server_threads = []
    for port in ports:
        try:
            server = ThreadedTCPServer((binding, int(port)), ThreadedTCPRequestHandler)
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            servers.append(server)
            server_threads.append(server_threads)
            print("Echo server running on: {0}:{1}".format(binding, port))
        except Exception:
            print("Listen on: {0}:{1} failed.".format(binding, port))
            if not ignore_failed_ports:
                break
    if server_threads:
        while True:
            try:
                time.sleep(60)
            except:
                print("Interrupted, shutdown servers...")
                for server in servers:
                    server.shutdown()
                print("done.")
                break
    else:
        print("None port listened.")
        os.sys.exit(1)

if __name__ == "__main__":
    run()
