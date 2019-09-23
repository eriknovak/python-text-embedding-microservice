# Document Embedding Microservice
Service for producing document representations via word embeddings.

## Prerequisites

- Create `.env` file in `microservice/config` folder. See instruction described [here](./microservice/config/).

- Python 3.* or higher (we recommend using Conda and creation of a separate enviroment for this project)

    To test that your python version is correct, run `python --version` in the command line


## Create an Environment and activate it

First create the virtual environment where the service will store all the modules.

```bash
pip install virtualenv
virtualenv -p python3 ./.venv
# on windows activate the environment
./.venv/Scripts/activate
# on UNIX activate the environment
. ./.venv/bin/activate
```

### Deactivating the environment

To deactivate the environment simply execute

```bash
deactivate
```

## Install

To install the project run

```bash
pip install -r requirements.txt
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

| Parameter               | Description                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| -H or --host            | The service host address (Default: '127.0.0.1')                                                                                 |
| -p or --port            | The service port (Default: 4000)                                                                                                |
| -e or --env             | The service environment. Options: 'production', 'development', 'testing' (Default: 'production')                                |
| -mp or --model_path     | The language model path (e.g. './data/embeddings/{insert.name.of.word.model}')                                                  |
| -mf or --model_format   | The language model type (see [Gensim](https://radimrehurek.com/gensim/)). Options: 'word2vec', 'fasttext' (Default: 'word2vec') |
| -ml or --model_language | The ISO 693-1 code of the language model (e.g. 'en' for English)                                                                |


##### Linux and Mac

```bash
python -m microservice.main start \
    -H localhost \
    -p 4000 \
    -mp ./data/embeddings/wiki.sl.align.vec \
    -ml sl
```

##### Windows

Afterwards run the following command from the root of the project. The parameters
can be changed.

```cmd
python -m microservice.main start -H localhost -p 4000 -mp ./data/embeddings/wiki.sl.align.vec -ml sl
```

#### Running different services

To run the same service on different models just change the `-p`, `-mp` and `-ml`
command line parameters and run the code.


### Running the service in Production Mode

Running the flask application in production mode requires some additional libraries.

#### Linux and Mac

To run the flask application in production we will use the following services available.

##### Gunicorn
[Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX. This is used to run the python script as a service.
It is quite easy to install and use.

1. Install gunicorn

    ```bash
    pip install gunicorn
    ```

2. Run the flask application with gunicorn. Change the parameters accordingly - but leave the `env` variable to be `'production'`.
    There are are two parameters that needs to be set.

    | Parameter | Description                                                                                                                                           |
    | ----------| ----------------------------------------------------------------------------------------------------------------------------------------------------- |
    | -w        | The number of workers working in parallel. More workers enable parallel request processing, but is limited by the number of processes the machine has |
    | -b        | The service address and port (e.g. '127.0.0.1:4000')                                                                                                  |


    An example of running the service with aligned Slovene language model from fasttext. **Note:** The address and port are the same in `-b` and the `create_app` value.

    ```bash
    gunicorn -w 4 -b 127.0.0.1:4000 'microservice:create_app(args={ "host":"127.0.0.1", "port":4000, "env":"production", "model_path":"./data/embeddings/wiki.sl.align.vec", "model_language":"sl", "model_format":"word2vec" })'
    ```

This is enough to support running the services in production, but to run multiple services at once the user
needs to open multiple terminals to run them. To run them in parallel in the background, use supervisor.

##### Supervisor: A Process Control System

[Supervisor](http://supervisord.org/) is a client/server system that allows its users to monitor
and control a number of processes on a UNIX-like operating systems.

1. Install supervisor
    ```bash
    sudo apt-get install supervisor
    sudo service supervisor start
    ```

2. Create a new file in `/etc/supervisor/conf.d` named `text_embeddings.conf` and copy the following code block. **Note:** the code block

    ```vim
    ;/etc/supervisor/conf.d/text_embeddings.conf
    [program:text_embedding_sl]
    user = {name-of-the-user}
    directory = /path/to/document-embedding-service
    command = sh ./scripts/environment.sh gunicorn -w 1 -b 127.0.0.1:4000 -c ./scripts/gunicorn.conf.py 'microservice:create_app(args={ "host":"127.0.0.1", "port":4000, "env":"production", "model_path":"./data/embeddings/wiki.sl.align.vec", "model_language": "sl", "model_format":"word2vec" })'

    priority = 900
    autostart = true
    autorestart = true
    stopsignal = TERM

    redirect_stderr = true
    stdout_logfile = /path/to/document-embedding-service/log/sl/%(program_name)s.log
    stderr_logfile = /path/to/document-embedding-service/log/sl/%(program_name)s.log
    ```

3. Update supervisor with the new configuration
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    ```
    At this point the services should already run. To stop and start the services use the following two commands:
    ```bash
    sudo supervisorctl stop text_embedding_sl  # stop the program called 'text_embedding_sl'
    sudo supervisorctl start text_embedding_sl # start the program called 'text_embedding_sl'
    ```

To run multiple services with different models/parameters modify the `/etc/supervisor/conf.d/text_embeddings.conf` file:

- copy the whole block starting from `[program:text_embedding_sl]`
- rename it to something else (e.g. `[program:text_embedding_en]` for English word embeddings)
- modify all of the upper parameters
- repeat step (3) in the supervisor setup process

Please not the following:

- The ports must be all different and available for use
- The number of workers in the `gunicorn` command must be less than the number of processers in the computer




#### Windows

**NOTE: If possible, run the service on a UNIX machine because it is easier.**

For windows running the flask service is a little more complicated. There are two approaches:

- Using apache + [mod_wsgi](https://pypi.org/project/mod-wsgi/)
- Installing a linux Virtual Machine (e.g. virtualbox) on the windows machine to host the application
   and proxy the requests from local IIS to the virtual system
