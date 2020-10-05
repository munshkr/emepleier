# EMEPLEIER

Send OSC messages to MPlayer

## Install

You will need Python 3, pip and mplayer.

### Python dependencies

Install first dependencies with Pip.

```bash
pip3 install --user -r requirements.txt
```

### Mplayer

#### Linux (Debian-based)

```bash
sudo apt-get install mplayer
```

#### OSX

Download [Mplayer OSC Extended](https://mplayerosx.ch/#downloads).

Make a symbolic link to the `mplayer` binary so you can start mplayer from the
command line.  For example:

```bash
ln -s /Applications/MPlayer\ OSX\ Extended.app/Contents/Resources/Binaries/mpextended.mpBinaries/Contents/MacOS/mplayer /usr/local/bin/mplayer
```

Test if it works by running `mplayer` from your terminal:

```bash
$ mplayer
MPlayer SVN-r38017-4.2.1 (C) 2000-2018 MPlayer Team
Usage:   mplayer [options] [url|path/]filename

Basic options: (complete list in the man page)
...
```

#### Windows

?


## Usage

In SuperCollider, start SuperDirt as usual, then execute the following:

```supercollider
~oscaddr = NetAddr.new("127.0.0.1", 5005);    // create the NetAddr

(
~video = "";
~dirt.receiveAction = { |event|
    var dur, nchan, vel, note, pchan;

    if (event['video'] != nil) {
        if (event.video != ~video) {
            event.postln;
            ~oscaddr.sendMsg("/loadfile", event.video);
            ~video = event.video;
        }
    };

    if (event['depth'] != nil && event['pos'] != nil && event['n'] != nil) {
        SystemClock.sched(event.latency, {
            ~oscaddr.sendMsg("/seek", (event.n + 1) * event.depth + event.pos);
        });
    }
};
)
```

Then, in Tidal, execute these:

```haskell
let pos = pF "pos"
    depth = pF "depth"
    video = pS "video"
```

Finally, supposing you have a directory `videos/` with some videos, run
emepleier passing some video to start playing first:

```bash
python3 ./emepleier.py videos/0001.mp4
```

## Example

```haskell
d1 $ n "0 1 2 1" # s "in" # depth 1.2 # pos "40 50" # video "0002.mp4"
```
