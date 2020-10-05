#!/usr/bin/env python
import argparse
import logging
import os
from subprocess import PIPE, Popen
from glob import glob

from pythonosc import dispatcher, osc_server

LINE_BUFFERED = 1


def start_mplayer(*, input_dir, host, port):
    def send_command(command):
        print(command)
        print(command, flush=True, file=process.stdin)

    def osc_seek(unused_addr, args, position):
        send_command('seek {} 1'.format(position))

    def osc_loadfile(unused_addr, args, name):
        send_command('loadfile {}'.format(name))

    dis = dispatcher.Dispatcher()
    dis.map('/seek', osc_seek, 'Seek')
    dis.map('/loadfile', osc_loadfile, 'Load File')

    server = osc_server.ThreadingOSCUDPServer((host, port), dis)
    print('Serving on {}'.format(server.server_address))

    blank_video_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'blank.mpeg')

    process = Popen(
        'mplayer -slave -idle -quiet -osdlevel 0 -fixed-vo'.split() +
        [blank_video_path],
        stdin=PIPE,
        universal_newlines=True,
        bufsize=LINE_BUFFERED,
        cwd=input_dir)

    server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_dir',
                        help='path to directory containing videos')
    parser.add_argument('--host',
                        '-H',
                        default='127.0.0.1',
                        help='The host/ip to listen on')
    parser.add_argument('--port',
                        '-P',
                        type=int,
                        default=5005,
                        help='The port to listen on')

    args = parser.parse_args()
    start_mplayer(input_dir=args.input_dir, host=args.host, port=args.port)
