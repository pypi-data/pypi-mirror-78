# Contrast Python Agent


## Overview

The Contrast Python agent provides runtime protection of Django, Flask and
Pyramid web applications.

## Online Documentation

For the most up to date documentation visit [Contrast Open Docs](https://docs.contrastsecurity.com/installation-python.html#python-overview)

### About Python

The Python agent is a WSGI- and framework-specific middleware that's compatible
with the most popular web application frameworks. The agent's goal is to be
fully WSGI compatible along with other web frameworks.

#### Protect Mode

In Protect mode, the Python agent inspects HTTP requests to identify
potentially harmful input vectors from its position within the middleware
stack. During the request, the agent monitors database queries, file writes and
other potentially damaging actions resulting from the request. At the end of
the request, the agent checks the rendered output for successful attacks, and
can block a successful attack from being forwarded to the application user. The
service sends the details of the attack to the Contrast application, which then
sends you an alert and displays attack details in the interface.

### Using the Agent

To start protecting your application, download the Python agent and create a
configuration file as described in the **Installation** section. The Python
agent is installed as a standard Python package, and communicates with a
standalone Contrast Service that runs outside your application.

## Supported Technologies

The Python agent supports Python versions 2.7+ and 3.5 to 3.8. It supports the
following web frameworks:

* Django: 1.10+, 2.0+, 3.0+ (Django 2 and 3 are Python 3 only)
* Flask: 0.10 - 0.12 and 1.0+
* Pyramid: 1.4.5 and 1.9+ (Beta)
* Pylons: 1.0+

>**Note:** The Python agent is meant to be WSGI compatible. It may be
compatible with other WSGI applications as long as the guidelines are followed.

### Database Support

The Python Agent has database support for:

* SQLite3 (`sqlite3` and `pysqlite2`)
* PostgreSQL (`psycopg2`)
* MySQL (`pymysql`)
* Cassandra 1.X (`pycassa`)

### NoSQL Support

The Python Agent has NoSQL support for:

* Mongo (`pymongo`)

### ORM Support

The Python Agent has ORM support for:

* SQLAlchemy (`SQLAlchemy`)
* Flask-SQLAlchemy (`Flask-SQLAlchemy`)

### OS Support

Agent testing is done on **64-bit OSX** and **64-bit Linux**. The agent has no
C dependencies, and may work in other operating system environments.


## Installation

To install the Contrast agent into your Python application, you must complete
the following steps.

1. Add *contrast-agent-[version].tar.gz* to the application's
*requirements.txt* (see **Standard Setup**).
2. Provide the agent with a valid *contrast_security.yaml* configuration file
(see **Configuration**).

### Standard Setup

The *contrast-agent-[version].tar.gz* is a standard packaged Python
library that you can add to the application's *requirements.txt*.

To use Contrast, add this line to your application's *requirements.txt* after
downloading the agent:

```
./path/to/contrast-agent-[version].tar.gz
```

After editing the *requirements.txt* you can install normally with:

``` bash
pip install -r requirements.txt
```

### Manual Setup

If you would prefer to install the Contrast agent manually, download the
*contrast-agent-[version].tar.gz* file to a local directory and run:

``` bash
pip install ./path/to/contrast-agent-[version].tar.gz
```

### Middleware Inclusion

To hook into incoming requests and outbound responses, you need to add the
Contrast middleware to your application. To do this, use the appropriate
guidance for your framework.

#### Django

For Django 1.10+,  2.0+, and 3.0+, add the following to your *settings.py* file:

``` python
MIDDLEWARE = [
  # OTHER MIDDLEWARE
  'contrast.agent.middlewares.django_middleware.DjangoMiddleware'
]
```

Older versions of Django have a different architecture for middlewares. For
Django 1.6 to 1.9, add the following in your *settings.py* file:

``` python
MIDDLEWARE_CLASSES = [
  # OTHER MIDDLEWARE
  'contrast.agent.middlewares.legacy_django_middleware.DjangoMiddleware'
]
```

#### Flask

``` python
import Flask
from contrast.agent.middlewares.flask_middleware import FlaskMiddleware as ContrastMiddleware

app = Flask(__name__)
app.wsgi_app = ContrastMiddleware(app)
```

#### Pyramid

``` python
from pyramid.config import Configurator

config = Configurator()
config.add_tween('contrast.agent.middlewares.pyramid_middleware.PyramidMiddleware')
```

#### WSGI

``` python
from contrast.agent.middlewares.wsgi_middleware import WSGIMiddleware as ContrastMiddleware

# other app code

app = get_wsgi_application()
app = ContrastMiddleware(app)
```

#### Pylons

``` python
from pylons.wsgiapp import PylonsApp
from contrast.agent.middlewares.wsgi_middleware import WSGIMiddleware as ContrastMiddleware

app = PylonsApp()
app = ContrastMiddleware(app)
```

### Next Steps

Once the installation process is complete, you must provide the agent with a
*contrast_security.yaml* configuration file as outlined in the
**Configuration** section below.


## Configuration

The Python agent and Contrast Service use a YAML file to configure their
behavior.

### File Location

The configuration file must be named *contrast_security.yaml* or
*contrast_security.yml* no matter where it's located. The Python agent loads
the configuration YAML from the following paths in order of precedence:

1. Any path saved in the environment variable `CONTRAST_CONFIG_PATH`
2. The settings directory within the current directory (e.g.,
*./settings/contrast_security.yaml*)
3. The current working directory (e.g., *./contrast_security.yaml*)
4. Within the server's *etc/contrast/python/* directory (e.g.,
*/etc/contrast/python/contrast_security.yaml*)
5. Within the server's *etc/contrast/* directory (e.g.,
*/etc/contrast/contrast_security.yaml*)

The agent and service may share a common configuration file, but only some
options and sections are applicable to each process.

### Configuration Options

Download a standard configuration file from the Contrast Dashboard. You must
place the file in one of the standard locations described above, and define the
following fields, at a minimum:

``` yaml
agent:
  service:
    host:
    port:
```

For additional information, see the [Contrast Open
Docs](https://docs.contrastsecurity.com/installation-pythonconfig.html).

### *Optional* Start the Service Manually
The Python agent will attempt to start the Contrast Service on it's own.
However, if you wish to run the Service separately please follow these steps.

Like the contrast-agent, the contrast-service requires a configuration
file. Place the configuration YAML file in the same directory as the
contrast-service.

The contrast-service is an executable Go Service that can be run directly from
the application directory. This can be done by executing:

- Linux/OSX:
    `./contrast-service`
- Windows:
    `./contrast-service.exe`
