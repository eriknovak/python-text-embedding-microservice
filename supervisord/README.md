# Supervisor File Creation

This folder contains all of the information for automatically create and copy the
supervisor configurations for running multiple text embedding services.

## Configurations

The scripts that create the supervisor configuration file all ready from a single
file - the `supervisor_config.json` file. This file has the following structure:


```js
{
  "text_embedding": {
    "{ISO 693-1 code language}": {
      "program": {string: program-name (must-be-unique)},
      "model_path": {string: path-to-the-model},
      "model_format": {string: model-format. Options: "word2vec", "fasttext"},
      "port": {number: port-number},
      "workers": {number: number-of-workers}
    },
    "{other ISO 693-1 code language}": {
        ...
    },
    ...
  },

  "interface": { (optional)
    "program": {string: program-name (must-be-unique)},
    "supervisord": { boolean: true-if-interface-should-get-proxy-config-from-supervisord-file },
    "port": {number: port-number},
    "workers": {number: number-of-workers}
  }

}
```

An example of such file is presented bellow:
```js
{
  "text_embedding": {
    "en": {
      "program": "text_embedding_en",
      "model_path": "./data/embeddings/wiki.en.align.vec",
      "model_format": "word2vec",
      "port": 4000,
      "workers": 1
    },
    "sl": {
      "program": "text_embedding_sl", # note that the program values are different
      "model_path": "./data/embeddings/wiki.sl.align.vec",
      "model_format": "word2vec",
      "port": 4001, # note that the port is different
      "workers": 1
    }
  },
  "interface": {
    "program": "text_embedding_interface",
    "supervisord": true,
    "port": 6000,
    "workers": 1
  }
}
```

## Creation Script

Once the configuration file is created, one can simply create the supervisor configuration
file with a simple command. The parameters it receives are:

| Parameter    | Description                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| -u or --user | The username that has access to the repository and will start the services                                                           |
| --interface  | If the interface configurations should be added to the `text_embedding.conf` file                                                    |
| -c or --copy | Copies the created `text_embedding.conf` to the `/etc/supervisord/conf.d` folder. User needs `sudo` privilages to do this (optional) |

```bash
[sudo] python create_supervisor_file.py -u {username} [--copy]
```
