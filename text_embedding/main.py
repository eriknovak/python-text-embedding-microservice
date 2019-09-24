import argparse
from text_embedding import create_app

if __name__=='__main__':
    # parse command line arguments
    argparser = argparse.ArgumentParser(description="Microservice for embedding text using word embedding models")
    subparsers = argparser.add_subparsers()

    argparser_production = subparsers.add_parser('start', help="Runs the service in the production environment")

    # the host and port of the text embedding microservice
    argparser_production.add_argument('-H', '--host', type=str, default='127.0.0.1', help="The host of the microservice")
    argparser_production.add_argument('-p', '--port', type=str, default='4000', help="The port of the microservice")
    argparser_production.add_argument('-e', '--env', type=str, default='production', help="The microservice environment")
    # the model parameters
    argparser_production.add_argument('-mp', '--model_path', type=str, help="The path to the word embedding model file")
    argparser_production.add_argument('-mf', '--model_format', type=str, default='word2vec', help="The format in which the language embedding model is saved. Possible options: 'word2vec' and 'fasttext' (default: 'word2vec')")
    argparser_production.add_argument('-ml', '--model_language', type=str, help="The ISO 693-1 code of the language embedding model")
    argparser_production.set_defaults(command='start')

    # parse the arguments and call whatever function was selected
    args = argparser.parse_args()

    if args.command == 'start':
        # get the arguments for creating the app
        arguments = {
            "host": args.host,
            "port": args.port,
            "env": args.env,
            "model_path": args.model_path,
            "model_format": args.model_format,
            "model_language": args.model_language
        }
        # create the application
        app = create_app(args=arguments)
        # run the application
        app.run(host=arguments["host"], port=arguments["port"])

    else:
        raise Exception('Argument command is unknown: {}'.format(args.command))