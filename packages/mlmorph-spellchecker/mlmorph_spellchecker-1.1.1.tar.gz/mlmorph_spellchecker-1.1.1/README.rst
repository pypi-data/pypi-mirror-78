Spellchecker based on Malayalam morphology analyser
===================================================

.. image:: https://img.shields.io/pypi/v/mlmorph-spellchecker.svg
    :target: https://pypi.python.org/pypi/mlmorph-spellchecker
    :alt: PyPI Version


This is a Spellchecker for Malayalam language based on `Malayalam morphology analyser - mlmorph`_.

Installation
------------

Python 3 is required. Using with `venv`_ is recommended

  .. code-block:: console

    $ pip install mlmorph_spellchecker

Usage
-----

  .. code-block:: python

    from mlmorph_spellchecker import SpellChecker
    spellchecker = SpellChecker()
    if spellchecker.spellcheck(word) is True:
        print('%s ✔️' % (word))
    else:
        print('%s ❌ Suggestions: %s' % (word, spellchecker.candidates(word)))

Command line interface
----------------------

  .. code-block:: console

    $ python -m mlmorph_spellchecker --help
    usage: __main__.py [-h] word

    positional arguments:
    word        word to spellcheck

    optional arguments:
    -h, --help  show this help message and exit

.. _`Malayalam morphology analyser - mlmorph`: https://gitlab.com/smc/mlmorph
.. _`venv`: https://docs.python.org/3/library/venv.html
