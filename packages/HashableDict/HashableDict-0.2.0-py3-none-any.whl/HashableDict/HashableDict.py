from collections.abc import Mapping, Hashable

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
        keys = set()
        for key, value in base_iterable:
            # wrap values in hashable boxes in case of mutability
            contents.add((key, HashBox(value)))
            keys.add(key)
        #use a frozenset internally because it is immutable
        self.__contents = frozenset(contents)
        self.__keys = frozenset(keys)

    def to_dict(self):
        '''
        Create a dict from self
        '''
        return dict(self.items())

    def items(self):
        '''
        Iterates through (key, value) pairs
        '''
        boxed_key_val_pairs = self._get_contents()
        for key, box in boxed_key_val_pairs:
            yield (key, box.contents)

    def keys(self):
        '''
        Returns the frozenset of keys in the dictionary
        '''
        return self.__keys

    def __iter__(self):
        '''
        Iterate through the dictionary keys in an unspecified order
        '''
        yield from self.keys()

    def __repr__(self):
        '''
        Return a string representation in the form
        'HashDict({key1: value1, key2: value2})'
        '''
        pairs = ((repr(key), repr(value)) for key, value in self.items())
        formatted_pairs = (f"{key}: {value}" for key, value in pairs)
        inner = ", ".join(formatted_pairs)
        return "HashDict({" + inner + "})"

    def __hash__(self):
        '''
        Hashes using a frozenset of dict keys
        '''
        return hash(self.keys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key_to_find):
        for key, value in self.items():
            if key == key_to_find:
                return value
        raise KeyError(key_to_find)

    def _get_contents(self):
        '''
        Return the internal __contents frozenset
        (such as for checking equality)
        '''
        return self.__contents

    @classmethod
    def fromkeys(cls, keys_iterable, value=None):
        '''
        Create a new dictionary with keys from iterable and values set to value.
        '''
        return HashDict((key, value) for key in keys_iterable)


class HashBox:
    '''
    A hashable container for storing something unhashable,
    Comparing equal to boxes with equal contents
    '''

    def __init__(self, contents=None):
        self.contents = contents

    def __repr__(self):
        return f"HashBox({repr(self.contents)})"

    def __hash__(self):
        '''
        All boxes will have a hash collision.
        '''
        return hash(0)

    def __eq__(self, other):
        '''
        Checks if other is a HashBox,
        And contains equal contents
        '''
        if not isinstance(other, HashBox):
            return NotImplemented
        return self.contents == other.contents
