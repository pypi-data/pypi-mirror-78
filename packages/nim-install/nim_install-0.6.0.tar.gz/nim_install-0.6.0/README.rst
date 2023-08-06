
This package can be used to install the nim compiler in a virtualenv::

   virtualenv /your/venv
   source /your/venv/bin/activate
   pip install nim-install
   nim_install
   nim --version

installs nim version 1.2.6, nimble, nimgrep and nimsuggest

If you want to install a different version run e.g.:

   nim_install 1.0.8

The compilation of nim is executed in parallel. Total installation time is about
40 seconds on my machine (including download time).
