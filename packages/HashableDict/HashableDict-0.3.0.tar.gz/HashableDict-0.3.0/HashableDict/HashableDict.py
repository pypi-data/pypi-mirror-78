from collections.abc import Mapping, Hashable
from abc import ABC, abstractmethod

HASH_BOX_XOR_MASK = 0b10101010101


class HashDict(Mapping, Hashable):
    '''
    An immutable dictionary that is hashable, even if its values are not.
    '''

    def __init__(self, base_iterable=None, **kwargs):
        '''
        HashDict() = empty dictionary
        HashDict(iterable)
            = dictionary with keys made from pairs in iterable
        HashDict(**kwargs) = dictionary made from kwargs
        '''
        assert not (base_iterable is not None and kwargs)
        if base_iterable is None:
            base_iterable = kwargs
        if isinstance(base_iterable, dict):
            base_iterable = base_iterable.items()
        contents = set()
        for key, value in base_iterable:
            # wrap values in hashable boxes in case of mutability
            contents.add(PairBox(key, value))
        # use a frozenset internally because it is immutable
        self.__contents = frozenset(contents)
        self.__hash = None

    @property
    def _contents(self):
        return self.__contents

    def __repr__(self):
        '''
        Return a string representation in the form
        'HashDict({key1: value1, key2: value2})'
        '''
        pairs = ((repr(key), repr(value)) for key, value in self.items())
        formatted_pairs = (f"{key}: {value}" for key, value in pairs)
        inner = ", ".join(formatted_pairs)
        return "HashDict({" + inner + "})"

    def __contains__(self, key):
        return MatchBox(key) in self._contents

    def __len__(self):
        return len(self._contents)

    def __iter__(self):
        for key, _ in self._contents:
            yield key

    def keys(self):
        for key, _ in self._contents:
            yield key

    def values(self):
        for _, value in self._contents:
            yield value

    def items(self):
        yield from map(tuple, self._contents)

    def __getitem__(self, key):
        matchbox = MatchBox(key)
        if matchbox in self._contents:
            results = matchbox.equal_elements
            return results[0].value
        raise KeyError(key)

    def __hash__(self):
        '''
        Hashes using a frozenset of dict keys
        '''
        if self.__hash is None:
            self.__hash = hash(self._contents)
        return self.__hash

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        if len(self) != len(other):
            return False
        for key, value in self.items():
            if key not in other or other[key] != value:
                return False
        else:
            return True

    @classmethod
    def fromkeys(cls, keys_iterable, value=None):
        '''
        Create a new dictionary with keys from iterable and values set to value.
        '''
        return HashDict((key, value) for key in keys_iterable)


class Box(ABC):
    def __hash__(self):
        '''
        Hashes based only on key, because value might be unhashable
        '''
        return HASH_BOX_XOR_MASK ^ hash(self.key)

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @property
    @abstractmethod
    def key(self):
        pass


class PairBox(Box):
    '''
    A hashable container for storing a key and an unhashable value,
    Comparing equal to boxes with equal keys
    '''

    def __init__(self, key, value=None):
        if not isinstance(key, Hashable):
            raise TypeError(f"Key {key} is not hashable")
        self.__key = key  # key should not be mutated
        self.value = value

    @property
    def key(self):
        return self.__key

    def __repr__(self):
        return f"PairBox({repr(self.key)}, {repr(self.value)})"

    def __eq__(self, other):
        '''
        Checks if other is a PairBox,
        And contains an equal key
        '''
        if not isinstance(other, PairBox):
            return NotImplemented
        return self.key == other.key

    __hash__ = Box.__hash__

    def __iter__(self):
        yield self.key
        yield self.value


class MatchBox(Box):
    '''
    Used for comparing with keys in a PairBox;
    Compares equal to PairBoxes with the same key,
    but stores everything it is compared with so that values can be retrieved.
    '''

    def __init__(self, key):
        if not isinstance(key, Hashable):
            raise TypeError(f"Key {key} is not hashable")
        self.__key = key
        self.equal_elements = []

    @property
    def key(self):
        return self.__key

    def __repr__(self):
        if not self.equal_elements:
            return f"MatchBox({repr(self.key)})"
        return f"MatchBox({repr(self.key)} has matched {self.equal_elements})"

    def __eq__(self, other):
        '''
        Checks self and other's .key attributes,
        but also stores other in a list for retrieval if self == other
        '''
        if not isinstance(other, Box):
            return NotImplemented
        elif self.key != other.key:
            return False
        if isinstance(other, PairBox):
            self.equal_elements.append(other)
        return True


    __hash__ = Box.__hash__
