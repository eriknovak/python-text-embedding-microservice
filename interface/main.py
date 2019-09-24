import argparse
from interface import create_app

#################################################
# Helper function
#################################################

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         my_dict = {}
         for kv in values.split(","):
             k,v = kv.split("=")
             my_dict[k] = v
         setattr(namespace, self.dest, my_dict)


if __name__=='__main__':
    # parse command line arguments
    argparser = argparse.ArgumentParser(description="Microservice for embedding text using word embedding models")
    subparsers = argparser.add_subparsers()

    argparser_production = subparsers.add_parser('start', help="Runs the service in the production environment")

    # the host and port of the text embedding microservice
    argparser_production.add_argument('-H', '--host', type=str, default='127.0.0.1', help="The host of the intefrace microservice")
    argparser_production.add_argument('-p', '--port', type=str, default='4200', help="The port of the interface microservice")
    argparser_production.add_argument('-e', '--env', type=str, default='production', help="The microservice environment")
    # the model parameters
    argparser_production.add_argument('-pr', '--proxy', dest="proxy", action=StoreDictKeyPair, help="The proxy configuration")
    argparser_production.add_argument('--supervisord', type=str2bool, nargs='?', const=True, default=False, help="Take the configurations from the supervisor config file")

    argparser_production.set_defaults(command='start')

    # parse the arguments and call whatever function was selected
    args = argparser.parse_args()

    if args.command == 'start':
        # get the arguments for creating the app
        arguments = {
            "host": args.host,
            "port": args.port,
            "env": args.env,
            "proxy": args.proxy,
            "supervisord": args.supervisord
        }
        # create the application
        app = create_app(args=arguments)
        # run the application
        app.run(host=arguments["host"], port=arguments["port"])

    else:
        raise Exception('Argument command is unknown: {}'.format(args.command))