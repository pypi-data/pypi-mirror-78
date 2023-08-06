import os
import sys
import time
from collections import defaultdict
from itertools import chain
from os.path import join, dirname, abspath, expanduser, expandvars, isfile

from utils import ClassFactory


class SubscribersBase:
    def _store_check(self, project, sid=None):
        raise NotImplementedError

    def _store_set(self, project, sid, lvl):
        raise NotImplementedError

    def _store_get(self, project, sid):
        raise NotImplementedError

    def _store_del(self, project, sid):
        raise NotImplementedError

    def _store_iter(self, project=None):
        raise NotImplementedError

    def _validate_project(self, project):
        assert isinstance(project, str), f'Project must be a string, but it `{type(project)}`'
        assert ' ' not in project, 'Forbidden symbol in project name'

    def _validate_sid(self, sid):
        assert isinstance(sid, int), f'Subscriber-id must be a number, but it `{type(sid)}`'

    async def sub(self, sid, project, lvl=3):
        if isinstance(lvl, str): lvl = int(lvl)
        self._validate_sid(sid)
        self._validate_project(project)
        assert lvl in (1, 2, 3, 4)
        self._store_set(project, sid, lvl)

    async def unsub(self, sid, project):
        self._validate_sid(sid)
        self._validate_project(project)
        self._store_del(project, sid)

    async def check_pub(self, project, lvl=3):
        self._validate_project(project)
        assert project != '*'
        assert lvl in (1, 2, 3, 4)
        if not self._store_check('*'):
            tArr1 = ()
        else:
            tArr1 = (sid for sid, lvl_max in self._store_iter('*') if lvl <= lvl_max)
        if not self._store_check(project):
            tArr2 = ()
        else:
            tArr2 = (sid for sid, lvl_max in self._store_iter(project) if lvl <= lvl_max)
        return chain(tArr1, tArr2) if tArr1 or tArr2 else ()


class SubscribersInMem(SubscribersBase):
    def __init__(self):
        self._map_byProject = defaultdict(dict)

    def _store_check(self, project, sid=None):
        if project not in self._map_byProject: return False
        if sid is not None and sid not in self._map_byProject: return False
        return True

    def _store_set(self, project, sid, lvl):
        try:
            assert self._map_byProject[project][sid] == lvl
            return False
        except (AssertionError, KeyError):
            self._map_byProject[project][sid] = lvl
            return True

    def _store_get(self, project, sid=None):
        if sid is None:
            return self._map_byProject[project]
        else:
            return self._map_byProject[project][sid]

    def _store_del(self, project, sid):
        try:
            assert (project not in self._map_byProject) or (sid not in self._map_byProject[project])
            return False
        except (AssertionError, KeyError):
            del self._map_byProject[project][sid]
            return True

    def __iter_all_projects(self):
        for project in self._map_byProject:
            for o in self._map_byProject[project].items():
                yield project, o

    def _store_iter(self, project=None):
        if project is None:
            return self.__iter_all_projects()
        else:
            return self._map_byProject[project].items()


class SubscribersPersistent(SubscribersBase):
    def __init__(self, *args, filePath=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__delimeter = ';'
        filePath = filePath or join(dirname(sys.argv[0]), 'subscribers.data')
        self.__filePath = abspath(expanduser(expandvars(filePath)))
        self.__fileObj = None
        if isfile(self.__filePath): self.__load()
        self.__fileObj = open(self.__filePath, 'w')
        self.__dump()

    def __load(self):
        mytime = time.time()
        bck = f'{self.__filePath}.bck'
        try:
            os.remove(bck)
        except FileNotFoundError:
            pass
        os.rename(self.__filePath, bck)
        i = 0
        with open(bck, 'r') as f:
            for line in f:
                if not line: continue
                a, line = line[0], line[1:]
                if a == '+':
                    project, sid, lvl = line.split(self.__delimeter, 2)
                    self._validate_project(project)
                    sid = int(sid)
                    self._validate_sid(sid)
                    lvl = int(lvl)
                    self._store_set(project, sid, lvl)
                elif a == '-':
                    project, sid = line.split(self.__delimeter, 1)
                    self._validate_project(project)
                    sid = int(sid)
                    self._validate_sid(sid)
                    self._store_del(project, sid)
                else:
                    raise ValueError(f'Unknow op-mode `{a}` for line `{line}`')
                i += 1
        print(f'SubscribersPersistent: Loaded {i} objects at {time.time() - mytime:.1f} seconds')

    def __dump(self):
        mytime = time.time()
        i = 0
        for project, (sid, lvl) in self._store_iter():
            self.__set(project, sid, lvl)
            i += 1
        print(f'SubscribersPersistent: Dumped {i} objects at {time.time() - mytime:.1f} seconds')

    def __set(self, project, sid, lvl):
        if not self.__fileObj: return
        s = self.__delimeter.join((
            str(project), str(sid), str(lvl)
        ))
        self.__fileObj.write(f'+{s}\n')
        self.__fileObj.flush()

    def __del(self, project, sid):
        if not self.__fileObj: return
        s = self.__delimeter.join((
            str(project), str(sid)
        ))
        self.__fileObj.write(f'-{s}\n')
        self.__fileObj.flush()

    def _validate_project(self, project):
        super()._validate_project(project)
        assert self.__delimeter not in project, 'Forbidden symbol in project name'

    def _store_set(self, project, sid, lvl):
        r = super()._store_set(project, sid, lvl)
        if r: self.__set(project, sid, lvl)
        return r

    def _store_del(self, project, sid):
        r = super()._store_del(project, sid)
        if r: self.__del(project, sid)
        return r


SubscribersDefault = ClassFactory(
    SubscribersBase,
    (SubscribersInMem, SubscribersPersistent),
    fixPrivateAttrs=False
)
