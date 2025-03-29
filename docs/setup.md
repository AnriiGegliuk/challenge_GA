# Environment Setup

In this project, the following environment is used:

- Python 3.12
- [uv](https://github.com/astral-sh/uv) A tool for managing Python packages and projects

## Setup Instructions

### Clone the Repository


```sh
$ git clone https://github.com/AnriiGegliuk/challenge_GA.git
```

### Install uv

For macOS or Linux, execute the following command:

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows, use PowerShell to execute the following command:

```ps1
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, you can verify that `uv` is installed correctly using the following command:

```sh
$ uv --version
```

### Create a Virtual Environment

```sh
$ cd challenge_GA # Move to the cloned directory
$ uv python install 3.12
$ uv python pin 3.12
$ uv sync
```
