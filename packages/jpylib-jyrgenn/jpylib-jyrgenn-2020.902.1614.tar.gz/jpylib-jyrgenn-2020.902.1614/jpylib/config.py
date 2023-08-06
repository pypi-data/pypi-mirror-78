# Config class with configuration file reader

import errno

from .namespace import Namespace
from .kvs import parse_kvs
# from .alerts import debug

class Config(Namespace):
    """Name space class used to build a config object."""

    def update(self, new_values, reject_unknown=True):
        super().update(new_values, skip_underscore=True,
                       reject_unknown=reject_unknown)

    def set(self, key, value, reject_unknown=True):
        if key not in self.__dict__ and reject_unknown:
            raise KeyError("variable not in config: " + repr(key))
        self.__dict__[key] = value

    def get(self, key):
        if key not in self.__dict__:
            raise KeyError("variable not in config: " + repr(key))
        return self.__dict__[key]

    def load_from(self, filename, reject_unknown=True, file_must_exist=True):
        """Read a configuration from file 'filename'."""
        try:
            with open(filename, "r") as f:
                contents = f.read()
        except FileNotFoundError as exc:
            if not file_must_exist:
                return None
            else:
                raise exc
        new_locals = {}
        try:
            exec(contents, globals(), new_locals)
        except Exception as e:
            raise type(e)("Error in config file: {}; {}".format(
                filename, e
            ))
        self.update(new_locals, reject_unknown=reject_unknown)
        return True

    def load_config_files(self, config_files, notice_func=None,
                          reject_unknown=True, files_must_exist=False):
        """Read the configuration from the config files.

        Optional "notice_func" is a function to print a message
        about a config file being loaded.

        """
        loaded = 0
        for file in config_files:
            if self.load_from(file, reject_unknown=reject_unknown,
                              file_must_exist=files_must_exist):
                loaded += 1
                if notice_func:
                    notice_func("configuration loaded from", file)
        return loaded

    def update_from_string(self, cfgstring, reject_unknown=True, intvals=True):
        """Update the configuration from a key-value string.

        This can be used to pass config snippets on the command line.
        The string can look like e.g. this:

        "foo=bar,dang=[1,2,15],d={a=b,c=[d,e,f],quux=blech},e=not"

        """
        self.update(parse_kvs(cfgstring, intvals=intvals),
                    reject_unknown=reject_unknown)
