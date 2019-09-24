import os
import json

def get_supervisord_proxy():
    """Get the supervisor configuration and refactor it as a proxy file

    Returns:
        dict: The dictionary showing the proxy configurations.

    """

    # check if the supervisor file exists
    if not os.path.isfile("./supervisord/supervisor_config.json"):
        return Exception("File './supervisord/supervisor_config.json' does not exist")

    # open the supervisor_config.json file
    with open("./supervisord/supervisor_config.json") as f:
        config = json.load(f)

    # assign the proxy placeholder
    proxy = { }

    if "text_embedding" in config:
        # iterate through the languages in the text_embedding languages
        for language in config["text_embedding"].keys():
            # iterate through the languages
            if language not in proxy:
                # assign the proxy - language to port
                proxy[language] = config["text_embedding"][language]["port"]

    # return the proxy configurations
    return proxy