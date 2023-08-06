import sys
import traceback
from urllib.parse import quote_plus
from urllib.parse import urljoin
from urllib.request import Request, urlopen

DEFAULT_TELEGATE_API = 'http://localhost:35001/api_v1/log'


def withMetaclass(meta, base):
    """
    Create a base class with a metaclass.

    This Code taken from `six` package.
    """
    orig_vars = base.__dict__.copy()
    slots = orig_vars.get('__slots__')
    if slots is not None:
        if isinstance(slots, str):
            slots = [slots]
        for slots_var in slots:
            orig_vars.pop(slots_var)
    orig_vars.pop('__dict__', None)
    orig_vars.pop('__weakref__', None)
    if hasattr(base, '__qualname__'):
        orig_vars['__qualname__'] = base.__qualname__
    return meta(base.__name__, base.__bases__, orig_vars)


def ClassFactory(base, extend, metaclass=None, fixPrivateAttrs=True):
    """ Возвращает новый класс, являющийся суб-классом от `base` и цепочки `extend`. """
    extend = (base,) + (tuple(extend) if extend else ())
    extend = tuple(reversed(extend))
    if metaclass:
        extend = tuple(withMetaclass(metaclass, o) for o in extend)
    name = '_'.join(cls.__name__ for cls in extend)
    attrs = {}
    if fixPrivateAttrs:
        # фиксит специфичный для питона подход к инкапсуляции атрибутов, добавляя поддержку специальных приватные атрибуты, начинающиеся на `___` (например self.___test). к ним можно получить доступ из любого суб-класс, но не извне
        # ~ оверхед для обычных приватных атрибутов отсутствует, для новых он порядка x10, такчто не стоит использовать их в критичных по скорости участках
        # ? одна из потенциальных оптимизаций: отказ от замыканий `bases`, `name`, `nCache` но пока неясно как это лучше сделать
        bases = [('_%s___' % cls.__name__, len(cls.__name__) + 4) for cls in extend]
        objSetM = object.__setattr__
        objGetM = object.__getattribute__
        objDelM = object.__delattr__
        nCache = {}

        def tFunc_setattr(self, key, val):
            if key in nCache:
                key = nCache[key]
            elif '___' in key:
                for s, l in bases:
                    if key[:l] != s: continue
                    k = key
                    key = '_' + name + '___' + key[l:]
                    nCache[k] = key
                    break
            return objSetM(self, key, val)

        def tFunc_getattr(self, key):
            key2 = None
            if key in nCache:
                key2 = nCache[key]
            elif '___' in key:
                for s, l in bases:
                    if key[:l] != s: continue
                    key2 = '_' + name + '___' + key[l:]
                    nCache[key] = key2
                    break
            if key2:
                return objGetM(self, key2)
            else:
                raise AttributeError("'%s' object has no attribute '%s'" % (name, key))

        def tFunc_delattr(self, key):
            if key in nCache:
                key = nCache[key]
            elif '___' in key:
                for s, l in bases:
                    if key[:l] != s: continue
                    k = key
                    key = '_' + name + '___' + key[l:]
                    nCache[k] = key
                    break
            return objDelM(self, key)

        attrs['__getattr__'] = tFunc_getattr
        attrs['__setattr__'] = tFunc_setattr
        attrs['__delattr__'] = tFunc_delattr
    cls = type(name, extend, attrs)
    return cls


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ErrorHandler(object):
    __metaclass__ = Singleton

    def __init__(self, cb=None, passErrorObjectToCB=False):
        self.cb = cb or self.cbDefault
        self.passErrorObjectToCB = passErrorObjectToCB
        sys.excepthook = self.__hook

    def __hook(self, *errObj):
        if issubclass(errObj[0], KeyboardInterrupt):
            return sys.__excepthook__(*errObj)
        if self.passErrorObjectToCB:
            self.cb(errObj)
        else:
            errStr = ''.join(traceback.format_exception(*errObj))
            self.cb(errStr)

    @classmethod
    def cbDefault(cls, err):
        isTerm = sys.stdout.isatty()
        if isTerm:
            err = f'\x1b[1m\x1b[31m{err}\x1b[0m'
        print(err)
        if isTerm:
            r = input('Programm paused, press any key to exit\nOr type "dbg" for starting debugger\n')
            if r and r.lower() == 'dbg':
                import pdb;
                pdb.pm()
            sys.exit(1)

    @classmethod
    def disable(cls):
        sys.excepthook = sys.__excepthook__


class ErrorLogger:
    def __init__(self, project, url=None):
        self._project = project
        assert self._project and isinstance(self._project, str)
        self._url = url or DEFAULT_TELEGATE_API
        assert self._url and isinstance(self._url, str)
        self._global_enabled = False

    @staticmethod
    def _logger(url, project, lvl, err=None, and_raise=False):
        assert url and isinstance(url, str)
        assert project and isinstance(project, str)
        assert (lvl or lvl == 0) and isinstance(project, (str, int))

        if not url.endswith('/'):
            url += '/'
        url = urljoin(url, project + '/' + str(lvl))

        if err is None:
            err = sys.exc_info()
        if isinstance(err, str):
            pass
        elif isinstance(err, tuple) and len(err) == 3 and isinstance(err[1], Exception):
            err = ''.join(traceback.format_exception(*err))
        else:
            raise TypeError(f'Unknown data type {type(err)}')

        data = f'```{err}```'
        data = quote_plus(data).encode('utf-8')
        headers = {'Content-Type': 'text/plain'}
        request = Request(url, data, headers=headers)
        r = urlopen(request).read().decode()
        if r:
            print(f'Response to logging to [{url}]\n{r}')
        if and_raise:
            raise RuntimeError(err) from None

    def error(self, data=None, and_raise=True):
        return self._logger(self._url, self._project, 'error', err=data, and_raise=and_raise)

    def warn(self, data=None):
        return self._logger(self._url, self._project, 'warn', err=data, and_raise=False)
    
    warning = warn

    def info(self, data):
        return self._logger(self._url, self._project, 'info', err=data, and_raise=False)

    def debug(self, data):
        return self._logger(self._url, self._project, 'debug', err=data, and_raise=False)

    def enable_global(self):
        if self._global_enabled: return
        ErrorHandler(self.error, passErrorObjectToCB=False)
        self._global_enabled = True
