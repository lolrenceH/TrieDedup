# Custom class restrictedListDict
# A class imitating a dict, store values in a list, with restricted keys
# use function restrictedListDict.addAllowedKeys("ATCGN") to add DNA bases and ambiguous base N
# @Author : Adam Yongxin Ye & Jianqiao Hu @ BCH

import warnings
import copy, sys


class restrictedListDict:
    """
    A class imitating a dict, store values in a list, with restricted keys
    
    Note: stored values should not be None
    """

    # Define class variables
    allowed_keys = []   # allowed keys shared by all restrictedListDict instances
    key2idx = {}   # a dict mapping from key to its index in allowed_keys
    default_value = None   # return a default value if query key cannot be found

    @classmethod
    def addAllowedKeys(cls, iterable):
        """
        Add keys in iterable to allowed_keys
        """
        for x in iterable:
            if x not in cls.key2idx:
                prevLen = len(cls.allowed_keys)
                cls.allowed_keys.append(x)
                cls.key2idx[x] = prevLen

    @classmethod
    def setDefaultValue(cls, value):
        """
        Set class variable default_value
        """
        cls.default_value = value

    __slots__ = 'storage'   # only one slot in each instance

    @classmethod
    def fromkeys(self, keys, value=None):
        """
        Return a restrictedListDict with the specified keys and the specified value
        """
        ans = restrictedListDict()
        for key in keys:
            ans[key] = value
        return ans

    def __init__(self):
        self.storage = []   # use list as the actual container

    def update(self, iterable):
        """
        Update the restrictedListDict with the specified key-value pairs
        """
        if isinstance(iterable, dict):
            iterable = iterable.items()
        for k, v in iterable:
            self[k] = v

    def __contains__(self, key):
        """
        Return whether the query key can be found in the restrictedListDict
        
        Note: stored values should not be None
        """
        if key in self.__class__.key2idx:
            idx = self.__class__.key2idx[key]
            if len(self.storage) > idx:
                if self.storage[idx] is not None:
                    return True
        return False

    def __len__(self):
        """
        Return the length of the storage list
        """
        return len(self.storage)   # simply the length of storage list, not actual how many stored keys

    def __setitem__(self, key, value):
        """
        Add/Set one key-value pair
        
        Note: use value = None to delete the key-value pair
        """
        if key in self.__class__.key2idx:
            idx = self.__class__.key2idx[key]
            prevLen = len(self.storage)
            if prevLen <= idx:   # extend the storage list if necessary, fill in None
                self.storage.extend([None] * (idx - prevLen + 1))
            self.storage[idx] = value
        else:
            warnings.warn(f'Key {key} is not allowed, so I just skip it', RuntimeWarning)

    def __getitem__(self, key, defaultvalue=None):
        """
        Retrieve the value of the query key
        
        Optional argument:
          defaultvalue=None, means to use class variable default_value instead
        
        Note: stored values should not be None
        """
        if key in self.__class__.key2idx:
            idx = self.__class__.key2idx[key]
            if key in self:
                return self.storage[idx]
            else:
                if defaultvalue is None:
                    defaultvalue = copy.copy(self.__class__.default_value)
                if defaultvalue is not None:
                    # self[key] = defaultvalue
                    prevLen = len(self.storage)
                    if prevLen <= idx:
                        self.storage.extend([None] * (idx - prevLen + 1))
                    self.storage[idx] = defaultvalue
                    return self.storage[idx]
                else:
                    # raise KeyError(f'Key {key} does not exist')
                    return None
        else:
            print(self.__class__.key2idx, file=sys.stderr)
            raise KeyError(f'Key {key} is not allowed')

    def get(self, key, defaultvalue=None):
        """
        Return the value of the specified key
        """
        return self.__getitem__(key, defaultvalue)

    def setdefault(self, key, defaultvalue=None):
        """
        Return the value of the specified key. If the key does not exist: insert the key, with the specified value
        """
        if key not in self:
            self[key] = defaultvalue
        return self[key]

    def __delitem__(self, key):
        """
        Delete a key-value pair by the query key; nearly equivalent to set value to None
        """
        if key in self.__class__.key2idx:
            idx = self.__class__.key2idx[key]
            prevLen = len(self.storage)
            if prevLen > idx:
                self.storage[idx] = None
        else:
            warnings.warn(f'Key {key} is not allowed, so I just skip it', RuntimeWarning)

    def pop(self, key):
        """
        Retrieve and delete a key-value pair by the query key
        """
        ans = None
        if key in self.__class__.key2idx:
            idx = self.__class__.key2idx[key]
            prevLen = len(self.storage)
            if prevLen > idx:
                ans = self.storage[idx]
                self.storage[idx] = None
        else:
            warnings.warn(f'Key {key} is not allowed, so I just skip it', RuntimeWarning)
        return ans

    def __iter__(self):
        """
        Return an iterator of the existing keys
        """
        for i in range(len(self.storage)):
            if self.storage[i] is not None:
                yield self.__class__.allowed_keys[i]

    def keys(self):
        """
        Return an iterator of the existing keys
        """
        return self.__iter__()

    def values(self):
        """
        Return an iterator of the existing values
        """
        for i in range(len(self.storage)):
            if self.storage[i] is not None:
                yield self.storage[i]

    def items(self):
        """
        Return an iterator of the existing key-value pairs
        """
        for i in range(len(self.storage)):
            if self.storage[i] is not None:
                yield (self.__class__.allowed_keys[i], self.storage[i])

    def clear(self):
        """
        Remove all the elements from the restrictedListDict
        """
        self.storage = []

    def copy(self):
        """
        Return a copy of the restrictedListDict
        """
        ans = restrictedListDict()
        ans.storage = copy.copy(self.storage)
        return ans

    def __str__(self):
        """
        Return the string representation of the restrictedListDict, like a dict
        """
        vec = []
        for k, v in self.items():
            vec.append(f'{k} : {v}')
        return '{' + ','.join(vec) + '}'

    def __repr__(self):
        """
        Return the string representation of the restrictedListDict, like a dict
        """
        return str(self)
