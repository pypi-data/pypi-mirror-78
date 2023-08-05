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

import re
import string
import collections


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model


DICTIONARY = []


def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in string.ascii_lowercase if b]
    inserts    = [a + c + b     for a, b in splits for c in string.ascii_lowercase]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in DICTIONARY)


def known(words):
    return set(w for w in words if w in DICTIONARY)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=DICTIONARY.get)


def is_correct(word):
    return word in DICTIONARY
