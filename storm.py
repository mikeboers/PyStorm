import os
import ctypes
from ctypes import c_void_p, byref

storm = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'libstorm.so'))

def _errcheck(result, func, args):
    print 'ERRCHECK', result, func, args
    return result

for name in '''

    SFileOpenArchive
    SFileCreateArchive
    SFileFlushArchive
    SFileCloseArchive
    
    SFileAddFileEx
    
'''.strip().split():
    func = getattr(storm, name)
    func.errcheck = _errcheck
    globals()[name] = func

    
class Archive(object):
    
    def __init__(self, path, mode='r', max_file_count=100):
        
        self.mode = mode
        if self.mode == 'r':
            self.handle = c_void_p()
            SFileOpenArchive(path, 0, 0, byref(self.handle))
        elif self.mode == 'w':
            self.handle = c_void_p()
            SFileCreateArchive(path, 0, max_file_count, byref(self.handle))
        else:
            raise ValueError('mode %r is not "r" or "w"' % mode)
    
    def close(self):
        if self.mode == 'w':
            SFileFlushArchive(self.handle)
        SFileCloseArchive(self.handle)
    
    def add_file(self, path, name=None):
        if name is None:
            name = path
        SFileAddFileEx(self.handle, path, name, 0, 0, 0)




