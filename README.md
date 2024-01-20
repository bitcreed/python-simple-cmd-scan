# Simple-Cmd-Scan

This is the developer guide. For a user guide, see README.rst.

Simple-cmd-scan is a command-line utility for scanning documents, offering a straightforward
alternative to GUI-based tools. Designed for simplicity and ease of use, it supports a range of
features for various scanning needs.

## Features

- **SANE-Supported Scanners**: Compatible with scanners that support the SANE backend.
- **Automated Document Feeder (ADF) Support**: Scan all documents from the ADF with the `-a` or `--adf` option.
- **Double-Sided Scanning**: Support for double-sided scanning with the `-d` or `--double-sided` option, including prompts for flipping the stack.
- **Multiple Document Handling**: Option to scan multiple documents continuously using `-m` or `--multidoc`, with the choice to `join` or `split` the output.
- **Custom Output Directory**: Specify an output directory for scanned documents using `-o` or `--output-dir`.
- **Find and List Scanners**: Easily find and list available scanners using `-f` or `--find-scanners`.
- **Select Scanner**: Choose a specific scanner with `-s` or `--scanner`.
- **Adjustable Log Level**: Control the log verbosity with `-l` or `--loglevel`.

## Installation

Installation for normal users:

```bash
pip install -e.
```

Dependency installation for development:

```bash
pip install -e.[dev]
```

## Usage

Run `simple-cmd-scan` with the desired options. For example:

```bash
simple-cmd-scan --adf --double-sided --multidoc join --output-dir /path/to/save
```


## Developers

bitcreed LLC is your open-source friendly software consulting company
sponsoring the development of this tool.
https://bitcreed.us

Contributers are most welcome to submit comments and PRs.
