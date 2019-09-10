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
Check the [configuration](./microservice/config/) folder to see what needs to be set before running the microservice
in development mode.


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


### Running the Service in Production Mode

To run the service in production mode, one must first change some parameters.

#### Linux and Mac

```bash
python -m microservice.execute start \
    -H localhost \
    -p 4001 \
    -mp ./data/embeddings/wiki.en.align.vec \
    -ml en
```

#### Windows

Afterwards run the following command from the root of the project. The parameters
can be changed.

```cmd
python -m microservice.execute start -H localhost -p 4001 -mp ./data/embeddings/wiki.en.align.vec -ml en
```

### Running different services

To run the same service on different models just change the `-p`, `-mp` and `-ml`
command line parameters and run the code.