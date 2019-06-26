#!/usr/bin/env python
from subprocess import Popen, PIPE
from pythonosc import dispatcher
from pythonosc import osc_server
import os
import argparse

LINE_BUFFERED = 1


def main(args):
    def send_command(command):
        print(command, flush=True, file=process.stdin)     

    def osc_seek(unused_addr, args, position):
        send_command('seek {} 1'.format(position))

    def osc_loadfile(unused_addr, args, name):
        print('Loading file', name)
        send_command('loadfile {}'.format(name))

    dis = dispatcher.Dispatcher()
    dis.map("/seek", osc_seek, "Seek")
    dis.map("/loadfile", osc_loadfile, "Loadfile")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dis)
    print("Serving on {}".format(server.server_address))

    cwd = os.path.dirname(args.filename)
    fname = os.path.basename(args.filename)

    process = Popen('mplayer -slave -quiet -fs -osdlevel 0 -fixed-vo'.split() + [fname], stdin=PIPE, universal_newlines=True, bufsize=LINE_BUFFERED, cwd=cwd)

    server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='filename', help='filename')
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")

    args = parser.parse_args()
    print('Argumetns', args)
    main(args)
