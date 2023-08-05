from . import Chibi_atlas
import copy


class Chibi_atlas_multi( Chibi_atlas ):
    def __setitem__( self, name, value ):
        if name in self:
            current = self[ name ]
            if not isinstance( current, list ):
                current = [ current ]
                del self[ name ]
                self[ name ] = current
            self[ name ].append( value )
        else:
            super().__setitem__( name, value )
