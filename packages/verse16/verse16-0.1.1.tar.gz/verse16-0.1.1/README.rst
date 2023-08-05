=======
verse16
=======


.. image:: https://img.shields.io/pypi/v/verse16.svg
        :target: https://pypi.python.org/pypi/verse16

.. image:: https://img.shields.io/travis/pelgo14/verse16.svg
        :target: https://travis-ci.com/pelgo14/verse16

.. image:: https://readthedocs.org/projects/verse16/badge/?version=latest
        :target: https://verse16.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

nlp rap text-generation


* Free software: BSD license
* Documentation: https://verse16.readthedocs.io.


Features
--------
Usage:

.. code-block::

  verse16 --help
  verse16 --lines 4
  verse16 --lines 16 --log_level DEBUG

GPU Support:

1. create environment.yml:

.. code-block::

  name: verse16
  dependencies:
      - python=3.7
      - tensorflow-gpu=1.15
  channels:
      - anaconda

2. ``conda env create -f environment.yml``

3. ``pip install verse16``

If you want to contribute
-------------------------
I am open to all ideas and contributions. contact me @ pelgo14@protonmail.com

Feature Ideas:

- implement for other languages (like german): https://huggingface.co/models?search=gpt2


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
