"""
Created by: Joanna Saikali
Purpose: Rewriting atomic writing of a file
"""

from atomicwrites import atomic_write as _backend_writer, AtomicWriter
from contextlib import contextmanager
import os
import tempfile
import io
from pathlib import Path


class SuffixWriter(AtomicWriter):
    def get_fileobject(self, dir=None, **kwargs):
        '''Return the temporary file to use.'''
        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))

        suffix = ''.join(Path(self._path).suffixes)  # Get the suffix of the desired target file, for example .txt or .tar.gz

        descriptor, name = tempfile.mkstemp(dir=dir, suffix=suffix)
        os.close(descriptor)
        kwargs['mode'] = self._mode
        kwargs['file'] = name
        return io.open(**kwargs)

@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):
    if mode!='w':
        raise Exception('invalid mode')

    with _backend_writer(file, writer_cls=SuffixWriter, **kwargs) as f:
        if as_file:
            yield f
        else:
            yield file
