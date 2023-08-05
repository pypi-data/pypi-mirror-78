import sys
import importlib.util
import copy
import json
import importlib
from chibi.file import Chibi_file
from chibi.atlas import _wrap


__all__ = [ 'Chibi_python' ]


class Chibi_python( Chibi_file ):
    def read( self ):
        value = super().read()
        return value

    def import_( self ):
        name = self.file_name[:-3]
        spec = importlib.util.spec_from_file_location(
            name, str( self.path.inflate ) )
        module = importlib.util.module_from_spec( spec )
        spec.loader.exec_module( module )
        return module
