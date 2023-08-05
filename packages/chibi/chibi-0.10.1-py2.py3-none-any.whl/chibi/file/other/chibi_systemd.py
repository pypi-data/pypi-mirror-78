import sys
import re
import importlib.util
import copy
import json
import importlib
from chibi.file import Chibi_file
from chibi.snippet.iter import chunk_each
from chibi.atlas.multi import Chibi_atlas_multi
from chibi.atlas import Chibi_atlas
from chibi.module import import_
from chibi.snippet.string import camel_to_snake


__all__ = [ 'Chibi_python' ]


category_regex = re.compile( r"\[.*\]" )


class Chibi_systemd( Chibi_file ):
    def read( self ):
        data = super().read()
        result = Chibi_atlas()
        lines = filter( bool, data.split( '\n' ) )
        lines = filter( lambda x: not x.startswith( '#' ), lines )
        chunks = chunk_each( lines, lambda x: category_regex.match( x ) )
        for section in chunks:
            section_key = section[0][1:-1].strip()
            section_data = section[1:]
            section_dict = Chibi_atlas_multi()
            for line in section_data:
                key, value = line.split( '=', 1 )
                key = key.strip()
                value = value.strip()
                if key in section_dict:
                    section_dict[key]
            result[ section_key.lower() ] = section_dict
        return result
