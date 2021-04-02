# Jira CLI

Simple Jira CLI client.

# Installation

Clone the repository

```bash
git clone https://github.com/dantonyuk/jira-cli.git
```

Set up virtual environment

```bash
cd jira-cli
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Run

To get help message just run the program without any arguments or with
`-h` or `--help` flag:

```bash
./jira --help
```

To get help about subcommand, run it with `-h` or `--help` flag:

```bash
./jira issue --help
```
