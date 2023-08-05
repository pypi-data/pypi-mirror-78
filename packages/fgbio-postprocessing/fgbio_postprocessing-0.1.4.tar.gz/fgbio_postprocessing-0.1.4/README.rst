====================
fgbio_postprocessing
====================


.. image:: https://img.shields.io/pypi/v/fgbio_postprocessing.svg
        :target: https://pypi.python.org/pypi/fgbio_postprocessing

.. image:: https://img.shields.io/travis/ionox0/fgbio_postprocessing.svg
        :target: https://travis-ci.com/ionox0/fgbio_postprocessing

.. image:: https://readthedocs.org/projects/fgbio-postprocessing/badge/?version=latest
        :target: https://fgbio-postprocessing.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Usage: simplex_filter [OPTIONS]

  Filter bam file to only simplex reads with `min_simplex_reads` on one
  strand

Options:
  --input_bam TEXT             Path to bam to be filtered  [required]
  --output_filename TEXT       Name of output bam  [required]
  --min_simplex_reads INTEGER  Minimum number of simplex reads to pass filter
  --help                       Show this message and exit.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
