Simple-Cmd-Scan User Documentation
==================================

Simple cmd (Command-Line) Scan is a simple command line utility to scan
documents. Just as simple-scan provides a nice UI, simple-cmd-scan provides
a nice command line alternative with a similarly (limited) set of features.

Usage
-----

To use simple-cmd-scan, run the command with desired options. For example:

.. code-block:: bash

   simple-cmd-scan --adf --double-sided

Configuration Options
---------------------

The following command-line options are available:

- ``-a`` or ``--adf``: Scan all documents from the Automated Document Feeder (ADF).
- ``-d`` or ``--double-sided``: Double-sided scan. Prompts the user to flip the stack, then merges pages.
- ``-m`` or ``--multidoc``: Keep scanning documents until the user aborts. Choices are 'join' (default) and 'split'.
- ``-o`` or ``--output-dir``: Specify the output directory for scanned documents.
- ``-f`` or ``--find-scanners``: Find and list scanners - no actual scanning.
- ``-s`` or ``--scanner``: Set the scanner to use.
- ``-l`` or ``--loglevel``: Set the log level (default is WARN).

Environment variables and a ``.env`` file can also be used for configuration.

Available Features
------------------

* SANE-Supported scanners
* Copy scanned documents to any mounted folder

Roadmap
-------

* None at this point

Out of Scope Items
------------------

* Translations - requires volunteers

Respects your Freedom
---------------------

bitcreed LLC and the developers of this tool hold themselves to high ethical
standards. Our commitment and promise to users are:
* No tracking - we want to hear what you like but we we'll never force tracking on you
* No ads - the product should be fun and productive to use - ads spoil both
