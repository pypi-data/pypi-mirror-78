=============
color-matcher
=============

Description
-----------

*color-matcher* enables color transfer across images which comes in handy for automatic color-grading
of photographs, paintings and film sequences as well as light-field and stopmotion corrections. The methods behind
the mappings are based on the approach from Reinhard *et al.*, the Monge-Kantorovich solution as proposed by
Pitie *et al.* and classical histogram matching.

|release| |build| |coverage| |pypi_total| |pypi|

Results
-------

|vspace|

.. list-table::
   :widths: 8 8 8 8
   :header-rows: 1
   :stub-columns: 1

   * -
     - Source
     - Target
     - Result
   * - Photograph
     - |src_photo|
     - |ref_photo|
     - |res_photo|
   * - Film sequence
     - |src_seq|
     - |ref_seq|
     - |res_seq|
   * - Light-field correction
     - |src_lfp|
     - |ref_lfp|
     - |res_lfp|
   * - Paintings
     - |src_paint|
     - |ref_paint|
     - |res_paint|

|

Installation
------------

* via pip:
    1. install with ``pip3 install color-matcher``
    2. type ``color-matcher -h`` to the command line once installation finished

* from source:
    1. install Python from https://www.python.org/
    2. download the source_ using ``git clone https://github.com/hahnec/color-matcher.git``
    3. go to the root directory ``cd color-matcher``
    4. load dependencies ``$ pip3 install -r requirements.txt``
    5. install with ``python3 setup.py install``
    6. if installation ran smoothly, enter ``color-matcher -h`` to the command line

Command Line Usage
==================

From the root directory of your downloaded repo, you can run the tool on the provided test data by

``color-matcher -s './test/data/scotland_house.png' -r './test/data/scotland_plain.png'``

on a UNIX system where the result is found at ``./test/data/``. A windows equivalent of the above command is

``color-matcher --src=".\\test\\data\\scotland_house.png" --ref=".\\test\\data\\scotland_plain.png"``

Alternatively, you can specify the method or select your images manually with

``color-matcher --win --method='hm-mkl-hm'``

More information on optional arguments, can be found using the help parameter

``color-matcher -h``

Author
------

`Christopher Hahne <http://www.christopherhahne.de/>`__

.. Hyperlink aliases

.. _source: https://github.com/hahnec/color-matcher/archive/master.zip

.. |src_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/scotland_house.png" width="200px" max-width:"100%">

.. |ref_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/scotland_plain.png" width="200px" max-width:"100%">

.. |res_photo| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/scotland_pitie.png" width="200px" max-width:"100%">

.. |src_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/parismusees/cezanne_paul_trois_baigneuses.png" width="200px" max-width:"100%">

.. |ref_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/parismusees/cezanne_paul_portrait_dambroise_vollard.png" width="200px" max-width:"100%">

.. |res_paint| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/parismusees/cezanne_paul_trois_baigneuses_mvgd.png" width="200px" max-width:"100%">

.. |src_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/wave.gif" width="200px" max-width:"100%">

.. |ref_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/sunrise.png" width="200px" max-width:"100%">

.. |res_seq| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/wave_mvgd.gif" width="200px" max-width:"100%">

.. |src_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/view_animation_7px.gif" width="200px" max-width:"100%">

.. |ref_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/bee_2.png" width="200px" max-width:"100%">

.. |res_lfp| raw:: html

    <img src="https://raw.githubusercontent.com/hahnec/color-matcher/master/test/data/view_animation_7px_hm-mkl-hm.gif" width="200px" max-width:"100%">

.. |vspace| raw:: latex

   \vspace{1mm}

.. Image substitutions

.. |release| image:: https://img.shields.io/github/v/release/hahnec/color-matcher?style=square
    :target: https://github.com/hahnec/color-matcher/releases/
    :alt: release

.. |build| image:: https://img.shields.io/travis/com/hahnec/color-matcher?style=square
    :target: https://travis-ci.com/github/hahnec/color-matcher

.. |coverage| image:: https://img.shields.io/coveralls/github/hahnec/color-matcher?style=square
    :target: https://coveralls.io/github/hahnec/color-matcher

.. |pypi| image:: https://img.shields.io/pypi/dm/color-matcher?label=PyPI%20downloads&style=square
    :target: https://pypi.org/project/color-matcher/
    :alt: PyPI Downloads

.. |pypi_total| image:: https://pepy.tech/badge/color-matcher?style=flat-square
    :target: https://pepy.tech/project/color-matcher
    :alt: PyPi Dl2