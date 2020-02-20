"""
pcf8591

Python library for generating OpenSCAD source, 
to be rendered and converted

home: https://www.github.com/wovo/3d
"""

from __future__ import annotations
from functools import reduce

# the default number of facets for a circle
number_of_circle_facets = 32

def _ssum( x ) -> string:
    """catenate a sequence of strings
    """
    return "".join( x )

def _indent( txt: string ) -> string:
    """return a text with all lines indented one ident step
    """
    return _ssum( map(
        lambda s: "   " + s + "\n",
            txt.split( "\n" )
    ))   
    
    
#============================================================================
# 
# shift: 2d /3d vector ADT
#
#============================================================================

class element:
    """OpenSCAD element that has a fixed string representation
    """
    
    def __init__( self, txt : string ):    
        self.txt = txt

    def __str__( self ) -> string:       
        return self.txt    
        
    def print( self, file_name ):
        f = open( file_name, "w" )
        f.write( str( self ) )
        f.close()       
        
        
    def __add__( self, rhs: element ) -> element:
        return element( 
            "union(){\n" + _indent( 
                str( self ) + "\n" + 
                str( rhs ) + "\n" ) +
            "}" )

    def __sub__( self, rhs: element ) -> element:
        return element( 
            "difference(){\n" + _indent( 
                str( self ) + "\n" + 
                str( rhs ) + "\n" ) +
            "}" )
              
    def __mul__( self, rhs: element ) -> element:
        return element( 
            "intersection(){\n" + _indent( 
                str( self ) + "\n" + 
                str( rhs ) + "\n" ) +
            "}" )        
    
    
#============================================================================
# 
# shift: 2d /3d vector ADT, and shift operation
#
#============================================================================

class shift:
    """2d or 3d vector
   
    This is a 2d (x,y) or 3d (x, y, z) vector.
    """
    
    def __init__( self, x, y, z = None ):
        """create from x and y, and optional z values
        """      
        if isinstance( x, shift ):
           self.x, self.y, self.z = x.x, x.y, x.z
        else:
           self.x, self.y, self.z = x, y, z
        
    def _add( self, a, b ):
       if a == None: return b
       if b == None: return a      
       return a + b       
   
    def __add__( self, rhs: xyz ):
        """add two shift values
        """   
        return shift( 
           self.x + rhs.x, 
           self.y + rhs.y, 
           self._add( self.z, rhs.z ) )
      
    def _mul( self, a, b ):
       if a == None: return None
       if b == None: return None   
       return a * b       
   
    def __mul__( self, v ):
        """multiply a shift by a scalar
        """   
        return shift( 
            self.x * v, 
            self.y * v, 
            self._mul( self.z, v ) )
      
    __rmul__ = __mul__      

    def __str__( self ):
        """convert to [ x, y ] or [ x, y, z ] string format
        """      
        if self.z == None:
            return "[ %f, %f ]" % ( self.x, self.y)
        else:
            return "[ %f, %f, %f ]" % ( self.x, self.y, self.z )
            
    def __pow__( self, m : element ) -> element:
        """apply the shift to an OpenSCAD element
        """        
        return element(
           ( "translate( %s )\n" % str( self ) ) +
               _indent( str( m ) ) )
      
def dup2( v ):
   return shift( v, v )

def dup3( v ):
   return shift( v, v, v )   
   
def x2( v ):
   return shift( v, 0 )

def y2( v ):
   return shift( 0, v )

def z3( v ):
   return shift( 0, 0, v )
      
   
#============================================================================
# 
# OpenSCAD basic 2D and 3D shapes
#
#============================================================================
      
class rectangle( element ): 
    """OpenSCAD square (bad name, I call it a rectangle) 
    """

    def __init__( self, x, y = None ):
        if y != None: x = shift( x, y )
        element.__init__( self, 
            "square( %s );" % str( x ))         
      
class box( element ): 
    """OpenSCAD cube (bad name, I call it a box) 
    """
    
    def __init__( self, x, y = None, z = None ):
        if y != None: x = shift( x, y, z )
        element.__init__( self, 
            "cube( %s );" % str( x ))
      
class circle( element ): 
    """OpenSCAD circle
    """
    
    def __init__( self, r, f = number_of_circle_facets ):
        element.__init__( self, 
            "circle( r=%f, $fn=%d );" % ( r, f ))          
     
class cylinder( element ): 
    """OpenSCAD cylinder
    """
    
    def __init__( self, r, h, f = number_of_circle_facets ):
        element.__init__( self, 
            "cylinder( r=%f, h=%f, $fn=%d );" % ( r, h, f ))        


#============================================================================
# 
# OpenSCAD operations
#
#============================================================================
      
class extrude:
    """OpenSCAD extrude operation
    """
    
    def __init__( self, z ):
        self.z = z   
         
    def __pow__( self, minion: element ) -> element:
        return element( 
            ( "linear_extrude( %f )\n" % self.z ) +
                _indent( str( minion ) ) )
        
class rotate:

    def __init__( self, x, y = None, z = None ):    
        if y != None:
           x = shift( x, y, z )
        self.angles = x

    def __pow__( self, minion: element ) -> element:   
        return element( 
            ( "rotate( %s )\n" % str( self.angles ) ) +
                _indent( str( minion ) ) )        
                    
     
#============================================================================
# 
# element manipulators
#
#============================================================================     
     
class repeat4:

    def __init__( self, x, y = None ):
       if y == None:
          self.x, self.y = x.x, x.y
       else:
          self.x, self.y = x, y

    def __pow__( self, minion: element ) -> element:   
      return (
         shift(      0,      0 ) ** minion +
         shift( self.x,      0 ) ** minion +
         shift(      0, self.y ) ** minion +
         shift( self.x, self.y ) ** minion
      )
           
           
#============================================================================
# 
# derived shapes
#
#============================================================================     

def chisel( size ) -> element:
   return rectangle( size ) - dup2( size) ** circle( size )
      
def rounded_rectangle( size: shift, rounding ) -> element:
   ch = chisel( rounding )
   return rectangle( size ) - ( 
      shift(      0,      0 ) ** rotate( 0, 0,    0 ) ** ch +
      shift(      0, size.y ) ** rotate( 0, 0,  -90 ) ** ch +
      shift( size.x, size.y ) ** rotate( 0, 0, -180 ) ** ch +
      shift( size.x,      0 ) ** rotate( 0, 0, -270 ) ** ch 
   )   
   
def bus( m, h ):
   return cylinder( m + 2, h ) - cylinder( m, h )   
      
      
#============================================================================
# 
# 
#
#============================================================================     
      
"""
c = repeat4( 10, 30 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
cx = xy( 0, 0 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
extrude( 15 )( circle( 3 ) ).print( "f2.scad" )

rounded_rectangle( xy( 10, 5 ), 2 ).print( "f.scad" )
      

pcb = xy( 78, 83 )
margin = 1
wall = 8
plate = pcb + 2 * dup2( margin ) * 2 + 2* dup2( wall )
bottom = box( set_z( plate, wall ))
bottom.print( "fx.scad" )
"""

x = rotate( 0, 90, 90 ) ** ( circle( 15 ) * rectangle( 15, 15 ) )
x = repeat4( 30, 30 ) ** ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
x =  rounded_rectangle( shift( 10, 20 ), 3 )

w = 2
m = 1
pcb = shift( 78, 83 )

x = \
   ( extrude( w ) ** rounded_rectangle( pcb + 2 * dup2( m + w ), 2 ) ) + \
   ( dup2( w + m ) + shift( 4, 3 ) ) ** repeat4( 71.5, 73.5 ) ** bus( 2, 8 )

x.print( "f.scad" )
      