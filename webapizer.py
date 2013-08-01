#!/usr/bin/env python
"""
Serve your awesome snippet via HTTP
"""
from gevent import monkey; monkey.patch_all()

import inspect
import functools
import importlib

import bottle


###############################################################################

#
# configurations
#
MODULES = ['os.path']

###############################################################################

# import all function from specified modules
modules = [importlib.import_module(m) for m in MODULES]
functions = [f for m in modules for f in vars(m).values() if inspect.isfunction(f)]

#
# helper functions
#
def generate_route(f):
    # get module name for specified function
    modulename = inspect.getmodule(f).__name__

    # get function name
    name = f.__name__

    # done
    return '/%s/%s' % (modulename, name)

#
# routes
#
@bottle.route('/', method=['GET'])
def index():
    """
    Display list of all available functions and their signature
    """
    template = """
        <h1>Webapizer Server</h1>
        <hr />
        <table>
            <tr>
                <th>Function</th>
                <th>Signature</th>
            </tr>
            % for url, signature in sorted(funclist):
            <tr>
                <td><a href="{{ url }}">{{ url }}</a></td>
                <td><pre>{{ signature }}</td>
            </tr>
            % end
        </table>
    """
    funclist = [(generate_route(f), repr(inspect.getargspec(f).args)) for f in functions]
    return bottle.template(template, funclist=funclist)

def handler(f, *args):
    """
    Invoke function with provided arguments
    """
    return f(*args, **bottle.request.params)

# register route for all functions
for f in functions:
    # generate route for this function
    route = generate_route(f)

    # register
    bottle.route(route, ['GET', 'POST'], functools.partial(handler, f))

###############################################################################

if __name__ == '__main__':
    # run
    bottle.run(host='localhost', port=8888, debug=True, server='gevent')
