#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from collections.abc import Iterable
from gym.spaces import Discrete



class FiniteSet(Discrete):
    r"""A discrete space in :math:`\{ a,b,c ... \}`. 
    Example::
        >>> space = FiniteSet('news')
        >>> space.sample()

    Warning: should not use a list/tuple/array as an element of the space.
    It is recommanded to use strings/characters
    """
    def __init__(self, actions):
        assert isinstance(actions, Iterable)
        self.__actions = tuple(actions)
        super(FiniteSet, self).__init__(len(actions))

    @property
    def actions(self):
        return self.__actions
    

    def sample(self):
        return self.np_random.choice(self.actions)

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.char in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return x in self.actions
        return 0 <= as_int < self.n

    def __repr__(self):
        return "FiniteSet(%d)" % self.n

    def __eq__(self, other):
        return isinstance(other, FiniteSet) and set(self.actions) == set(other.actions)

    def __getitem__(self, k):
        return self.actions[k]

    def encode(self, k=None, encoder=None):
        """Encode the space with numbers
        
        Keyword Arguments:
            k {int} -- the index of an element (default: {None})
            encoder {object} -- An encoder with scikit-learn apis,
            such as OneHotEncoder (default: {None})
        
        Returns:
            np.ndarray -- the result of encoding
        """
        if k is None:
            X = [[a] for a in self.actions]
            self.encoder = encoder.fit(X)
            return self.encoder.transform(X).toarray()
        else:
            if not hasattr(self, 'encoder'):
                self.encode()
            if isinstance(k, int):
                return self.onehot[k]
            elif isinstance(k, (list, tuple, np.ndarray)):
                return self.encoder.transform([[_] for _ in k]).toarray()
            else:
                return self.encoder.transform([[k]]).toarray()[0]

