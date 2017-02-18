# dkron-cli

Command line interface client for [Dkron](http://dkron.io/).

### Prerequisites

* Pytnon 3

### Installing

To install use pip:

```console
pip install dkron-cli
```

Or clone the repo:

```console
git clone https://github.com/Eyjafjallajokull/dkron-cli.git
python setup.py install
```

### Usage

Before you begin, set environment variable `DKRON_API_URL` to point running dkron instance.

```console
export DKRON_API_URL=http://my-dkron.example.com
```

Alternatively, you can instert `--url` argument to every invocation of dkron-cli.

#### Fetch all jobs

```console
dkron-cli get jobs
```

#### Fetch specific job

```console
dkron-cli get job [job_name]
```

#### Create or update job

```console
dkron-cli apply job [json_file] ...
```

You can pass multiple files at once.

#### Delete job

```console
dkron-cli delete job [job_name]
```
