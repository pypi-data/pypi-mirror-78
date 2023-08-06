# Standard Library
from typing import Union, List

# Thrid Party
from pylatex import Package
from pylatex.base_classes import CommandBase, Arguments

# Local
from rewrite.tex.texlist import TexList


class ProvideBool(CommandBase):
    """A command that defines a new boolean flag unless it has already been defined."""

    packages = [Package('etoolbox')]

    def __init__(self, bool_name: str, **kwargs):
        self.bool_name = bool_name
        super().__init__(arguments=bool_name, **kwargs)

# Future tests
"""
# Test
ProvideBool('hi').dumps()
# Result
'\\providebool{hi}'
"""


class SetBool(CommandBase):
    """A command that sets the value of an existing boolean flag."""

    packages = [Package('etoolbox')]

    def __init__(self, bool_name: str, value: bool):
        self.bool_name = bool_name
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        tex_bool = {True:'true', False:'false'}
        arguments = [self.bool_name, tex_bool[value]]
        super().__init__(arguments=arguments)
        self._value = value

# Future tests
"""
# Test
SetBool('hi', True).dumps()
# Result
'\\setbool{hi}{true}'
"""

class IfBool(CommandBase):
    """A command that conditionally runs TeX based on the value of a boolean flag."""

    packages = [Package('etoolbox')]

    def __init__(self, bool_name: str, if_true: List[object], if_false: List[object] = None, **kwargs):
        self.bool_name = bool_name

        # if_true and if_false should be a list of TeX commands to be run in order
        if_true = TexList(data=if_true)
        self.if_true = if_true
        if_false = TexList(data=if_false)
        self.if_false = if_false
        super().__init__(arguments=Arguments(bool_name, if_true, if_false), **kwargs)

# Future tests
"""
# Setup
from pylatex.utils import bold

# Test
IfBool('hi', 'Run me if True', 'Run me if False').dumps()
# Result
'\\ifbool{hi}{Run me if True}{Run me if False}'

# Test
IfBool('hi', bold('Run me if True'), ['Run me if False', 'Run me too!']).dumps()
# Result
'\\ifbool{hi}{\\textbf{Run me if True}}{Run me if False%\nRun me too!}' #<-------------- Not sure if this will run the way I expect because of the `%`
"""