# Decentralized Timeline
A peer-to-peer decentralized timeline using [Python's implementation of the Kademlia DHT](https://github.com/bmuller/kademlia), [asyncio](https://docs.python.org/3/library/asyncio.html) and [sqlite3](https://docs.python.org/3/library/sqlite3.html).

A detailed description of the project is available in the [docs directory](docs/presentation.pdf).

**Group members**:
1. [Alexandre Abreu](https://github.com/a3brx)
2. [Diana Freitas](https://github.com/dianaamfr)
3. [Juliane Marubayashi](https://github.com/Jumaruba)
4. [Simão Lúcio](https://github.com/yolonhese)

## Instalation

To install the program you must clone the repository and install its dependencies.

Assumming you have [pipenv](https://pypi.org/project/pipenv/) installed, just run the following commands:

```console
$ git clone https://github.com/dianaamfr/decentralized-timeline.git
$ pipenv install
```

The following command must be executed in every shell:

```console
$ pipenv shell
```

## Execution

The repository already has default configurations in the [config folder](config/), so it can be run as described below.

Start by creating a bootstrap peer:

```console
$ python -m src.bootstrap
```

Then, start as many peers as you want with different addresses, using the following command:

```console
$ python -m src 127.0.0.1 3000
```

With _127.0.0.1_ as IP and _3000_ as port.

## Cleaning

To clean the temporary files created after the execution, just run:

```console
$ make clean
```