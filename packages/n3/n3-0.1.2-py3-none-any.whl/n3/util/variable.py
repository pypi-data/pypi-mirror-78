import abc
import os
import types
import typing


class Vars(metaclass=abc.ABCMeta):
    def attach_parser(self, parser):
        for k, v in self._dict().items():
            kwargs = {}

            help_key = f'_{k}_help'
            if hasattr(self, help_key):
                kwargs['help'] = getattr(self, help_key)

            keyword_key = f'_{k}_is_keyword'
            is_keyword = not (hasattr(self, keyword_key)
                              and not getattr(self, keyword_key))
            if is_keyword:
                keys = [f'--{k}']
                shortcut_key = f'_{k}_shortcut'
                if hasattr(self, shortcut_key):
                    keys.append(f'-{getattr(self, shortcut_key).lower()}')
            else:
                keys = [k]

            if v is not None:
                required = False
                ty = v.__class__
            else:
                required = True
                ty = getattr(self, f'_{k}_type')

            if is_keyword:
                kwargs['required'] = required

            if issubclass(ty, (list, set)):
                parser.add_argument(*keys, nargs='+', **kwargs)
            else:
                parser.add_argument(*keys, type=ty, **kwargs)

    def apply(self, args):
        for k in self._keys():
            v = getattr(args, k)
            if v is None:
                continue
            if isinstance(getattr(self, k), set):
                v = set(v)
            setattr(self, k, v)

    def _assert_not_none(self, name):
        for key in self._keys():
            value = getattr(self, key)
            if value is None:
                raise Exception(f'not defined in {name}: {key}')

    def _keys(self):
        if hasattr(self, '_order'):
            return self._order
        return [k for k in dir(self) if
                not k.startswith('_') and
                not isinstance(getattr(self, k), types.MethodType)]

    def _dict(self):
        return {k: getattr(self, k) for k in self._keys()}

    def __repr__(self):
        return repr(self._dict())


class EnvVars(Vars, metaclass=abc.ABCMeta):
    def load_env(self):
        for key_origin in self._keys():
            key = f'N3_{key_origin.upper()}'
            if key in os.environ:
                value = os.environ[key]
                origin = getattr(self, key_origin)

                if isinstance(origin, (list, set)):
                    value = [v.strip() for v in value.split(',')]
                    if isinstance(origin, set):
                        value = set(value)
                elif origin is not None and not isinstance(origin, type(value)):
                    raise Exception(
                        f'unexpected type for "{key_origin}": "{type(origin).__name__}"')
                setattr(self, key_origin, value)
