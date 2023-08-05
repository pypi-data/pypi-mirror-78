pyimgconvert 1.0.10
===================

Quick Overview
--------------

Python wrapper around Linux CLI "convert" which works as an entrypoint around the Linux image processing 'ImageMagick'.

Overview
--------

``pyimgconvert`` is a Python utility which acts as a wrapper around the ``magick convert`` Linux CLI program that is useful for convert input images to the desired format and saves them in an output directory specified by the user.

This utility requires you to pass an ``inputDir``, ``inputFile``, ``outputDir``, ``outputFile``, and all the other optional CLI arguments that the ``convert`` accepts as a string to the ``args`` argument of ``pyimgconvert``. 

Assumptions
-----------

This document assumes UNIX conventions and a ``bash`` shell. The script should work fine under Windows, but we have not actively tested on that platform -- our dev envs are Linux Ubuntu and macOS.

Installation
~~~~~~~~~~~~

Python module
~~~~~~~~~~~~~

One method of installing this script and all of its dependencies is by fetching it from `PyPI <https://pypi.org/project/pyimgconvert/>`_.

.. code:: bash

        pip3 install pyimgconvert

Docker container
~~~~~~~~~~~~~~~~

We also offer a docker container of ``pyimgconvert`` as a ChRIS-conformant platform plugin here https://github.com/FNNDSC/pl-imageconvert -- please consult that page for information on running the dockerized container. The containerized version exposes a similar CLI and functionality as this module.

How to Use
----------

``mgz2imgslices`` needs at a minimum the following required command line arguments:

- ``-I | --inputDir <inputDir>``: The input directory which contains the input image that is to be converted

- ``-i | --inputFile <inputFile>``: The input image file to convert.

- ``-O| --outputDir <outputDir>``: The output directory which will store the output image

- ``-o | --outputFile <outputFile>``: The output file name (with extension) to save the output image

- Optional: ``-a | --args "ARGS: <otherArgs>"``: Pass all the other arguments that ``convert`` accepts to this argument using the double quotes.

Examples
--------

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

- Make sure your current working directory is ``devel``. At this juncture it should contain the image file that you want to convert.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

**Example-1**

.. code:: bash

    pyimgconvert 
        --inputDir ${DEVEL}/                \
        --inputFile image.jpg               \
        --outputDir ${DEVEL}/results/       \
        --outputFile image.png              \

**Example-2**

.. code:: bash

    pyimgconvert 
        --inputDir ${DEVEL}/                            \
        --inputFile image.jpg                           \
        --outputDir ${DEVEL}/results/                   \
        --outputFile image.png                          \
        --args "ARGS: -colorspace RGB    -resize 40% "  

- The output image will be stored in the ``results`` directory. 
