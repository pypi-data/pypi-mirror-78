"""
Copyright (C) 2019  Universite catholique de Louvain, Belgium.

This file is part of CP3SlurmUtils.

CP3SlurmUtils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CP3SlurmUtils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CP3SlurmUtils.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys


def interactiveYesNoQuestion(question, default='no', answerYes=False):
    """Ask a yes/no question and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    validAnswers = {'yes': True, 'y': True, 'no': False, 'n': False}
    if answerYes:
        return validAnswers['yes']
    prompt = " [y/n] "
    if default in ['yes', 'y']:
        prompt = " [Y/n] "
    if default in ['no', 'n']:
        prompt = " [y/N] "
    while True:
        sys.stdout.write(question + prompt)
        try:
            # Python 2
            _input = raw_input
        except NameError:
            # Python 3
            _input = input
        choice = _input().lower()
        if choice in validAnswers:
            return validAnswers[choice]
        elif choice == '' and default is not None:
            return validAnswers[default]
        else:
            sys.stdout.write("Please respond with 'yes' ('y') or 'no' ('n').\n")


class TimeoutException(Exception):
    pass


def questionTimeoutHandler(signum, frame):
    msg = "\nSorry, the timeout limit to answer the question has been reached."
    raise TimeoutException(msg)
