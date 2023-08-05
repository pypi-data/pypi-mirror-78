
#
#   YaLafi module for LaTeX package amsthm
#

from yalafi.defs import ModParm, Environ

require_packages = []

def modify_parameters(parms):

    macros_latex = r"""

        \newcommand{\qedhere}{}
        \newcommand{\theoremstyle}[1]{}

    """

    macros_python = []

    environments = [

        Environ(parms, 'proof', args='O',
                            # Parser.expand_arguments() may skip space
                            repl='#1.\n', defaults=[parms.proof_name]),

    ]

    return ModParm(macros_latex=macros_latex, macros_python=macros_python,
                        environments=environments)

