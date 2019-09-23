# Document Embedding Microservice
Service for producing document representations via word embeddings.

## Prerequisites

- Create `.env` file in `microservice/config` folder. See instruction described [here](./microservice/config/).

- Python 3.* or higher (we recommend using Conda and creation of a separate enviroment for this project)

    To test that your python version is correct, run `python --version` in the command line

## Install

To install the project run

```bash
pip install -r requirements.txt
# if using conda
conda install --file requirements.txt
```

## Starting Microservice

To start the microservice one must first initialize some global variables.

### Linux and Mac

```bash
export FLASK_APP=microservice
export FLASK_ENV=development
```

### Windows

For Windows cmd, use `set` instead of `export`:

```cmd
set FLASK_APP=microservice
set FLASK_ENV=development
```

For Windows PowerShell, use `$env:` instead of `export`:

```PowerShell
$env:FLASK_APP="microservice"
$env:FLASK_ENV="development"
```

### Running the Service in Development Mode
The above configuration will set the application to run in development mode.
Development mode shows an interactive debugger whenever a page raises an exception,
and restarts the server whenever you make changes to the code.
One can leave it running and just reload the browser page as one does changes to the service.

#### Prerequisites
Check the [configuration](./microservice/config/) folder to see what needs to be set before running
the microservice in development mode.


To run the service:
```bash
# the python -m enables auto-reload on file changes
python -m flask run
```

One will see output similar to this:

```bash
 * Serving Flask app "microservice" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 317-565-965
```
Visit `http://localhost:5000/` (or `http://127.0.0.1:5000/`) in a browser to see the Flask web
application.


#### Alternatives

To give more control, the user can provide additional parameters to the service. What follows are
instructions on how to run the service in development mode with additional parameters.

##### Linux and Mac

```bash
python -m microservice.execute start \
    -H localhost \
    -p 4001 \
    -mp ./data/embeddings/wiki.en.align.vec \
    -ml en
```

##### Windows

Afterwards run the following command from the root of the project. The parameters
can be changed.

```cmd
python -m microservice.execute start -H localhost -p 4001 -mp ./data/embeddings/wiki.en.align.vec -ml en
```

### Running different services

To run the same service on different models just change the `-p`, `-mp` and `-ml`
command line parameters and run the code.


### Running the service in Production Mode

Running the flask application in production mode requires some additional libraries.

#### Linux and Mac

To run the flask application in production, checkout this [article](https://medium.com/@thucnc/deploy-a-python-flask-restful-api-app-with-gunicorn-supervisor-and-nginx-62b20d62691f) for
guidelines.

##### Gunicorn
[Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX. It is quite easy to install
and use.

1. Install gunicorn

    ```bash
    pip install gunicorn
    ```

2. Run the flask application with gunicorn

    ```bash
    gunicorn -w 4 -b 127.0.0.1:4000 microservice:execute
    ```

##### Supervisor: A Process Control System

[Supervisor](http://supervisord.org/) is a client/server system that allows its users to monitor
and control a number of processes on a UNIX-like operating systems.

1. Install supervisor
    ```bash
    pip install supervisor
    ```



#### Windows

**NOTE: If possible, run the service on a UNIX machine because it is easier.**

For windows running the flask service is a little more complicated. There are two approaches:

- Using apache + [mod_wsgi](https://pypi.org/project/mod-wsgi/)
- Installing a linux Virtual Machine (e.g. virtualbox) on the windows machine to host the application
   and proxy the requests from local IIS to the virtual system





