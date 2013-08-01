webapizer
=========

Ever had the need to access your snippet function via web? (eg. Google Refine) This project implements a minimal web server to allow you to interface with your favorite Python function through HTTP protocol at very high concurrency (courtesy of gevent).

Clone this repository and start serving your awesome snippet via HTTP!

Example Usage
-------------

```
$ webapizer.py
Bottle v0.11.6 server starting up (using GeventServer())...
Listening on http://localhost:8888/
Hit Ctrl-C to quit.
```

Next, access os.path.normpath() function at http://localhost:8888/ntpath/normpath?path=/test/../x (note: namespace may vary on different platform)