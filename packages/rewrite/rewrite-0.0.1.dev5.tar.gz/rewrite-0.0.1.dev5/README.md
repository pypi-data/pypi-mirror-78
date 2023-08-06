ReWrite
=======

ReWrite is a Python package for generating PDF documents via LaTeX. The goal of this project is to allow instructors to recreate course documents that must change in routine ways every time the course is offered. My vision is for ReWrite to support the creating of randomizable math problems and assessments without extensive programming knowledge.

Acknowledgments
---------------

The previous name of this package was ExamSage which was a tribute to  William Stein's [SageMath](http://www.sagemath.org/) project. Stein also developed the [CoCalc](https://cocalc.com/) platform. Without Stein's contributions to the open source community, ReWrite may have never moved beyond a pure LaTeX solution.

ReWrite interfaces with LaTeX via Jelte Fennema's [PyLaTeX](https://jeltef.github.io/PyLaTeX/) library. Many of the classes provided by ReWrite inherit from classes provided by PyLaTeX. Also, much of my documentation design choices are modeled on the PyLaTeX documentation.

Warning
-------

This is my second package and is intended as a learning exercise. In other words, expect nothing to work and everything to change.


Installation
------------

ReWrite is being developed on [CoCalc](https://cocalc.com/) in Python 3.6.7 and it can be installed by running:

    pip3 install rewrite


Support
-------

If you are having issues, please let me know at mbarnard10@ivytech.edu


License
-------

The project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.
