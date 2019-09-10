# Embedding Models

This folder contains the files containing the language embedding models.

## Model Format

The first line gives the number of vectors and their dimension. The other lines
contain a word followed by its vector. Each value is space separated.

## FastText pre-generated models

One source of language models is the pre-generated fasttext models.

One can download them from the following links:

| Model         | Description                                                   | Link                                             |
| ------------- | ------------------------------------------------------------- | ------------------------------------------------ |
| English       | The english embeddings generated on different data sources    | https://fasttext.cc/docs/en/english-vectors.html |
| 157 languages | The embeddings for 157 langs trained on Wiki and Common Crawl | https://fasttext.cc/docs/en/crawl-vectors.html   |
| Aligned       | The aligned word embeddings for 44 languages                  | https://fasttext.cc/docs/en/aligned-vectors.html |

### License

**Last Check 10.09.2019**:
These word vectors are distributed under the [Creative Commons Attribution-Share-Alike License 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
