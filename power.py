"""
pcf8591

Python library for generating OpenScad

home: https://www.github.com/wovo/3d
"""

from __future__ import annotations
from functools import reduce

# the default number of facets for a circle
number_of_circle_facets = 32

def ssum( x ):
    """catenate a sequence of strings
    """
    return "".join( x )

    
#============================================================================
# 
# 2d and 3d ADTs
#
#============================================================================

class xy:
    """2d vector
    
    This is a 2d (x,y) vector.
    """

    def __init__( self, x, y ):
        """create from x and y values
        """
        self.x, self.y = x, y
   
    def __add__( self, rhs: xy ) -> xy:
        """add two xy values
        """
        return xy( self.x + rhs.x, self.y + rhs.y )
      
    def __mul__( self, v ) -> xy:
        """multiply an xy by a scalar
        """
        return xy( self.x * v, self.y * v )
      
    __rmul__ = __mul__
      
    def __str__( self ) -> string:
        """convert to [ x, y ] string format
        """
        return( "[ %f, %f ]" % ( self.x, self.y ) )  
      
    def __call__( self, rhs: element ) -> element:   
        """shift (translate) the argument 
        """    
        return element_shift( xyz( self.x, self.y, 0 ), rhs )            

class xyz:

   def __init__( self, x, y, z ):
      self.x, self.y, self.z = x, y, z
   
   def __add__( self, rhs: xyz ):
      return xyz( self.x + rhs.x, self.y + rhs.y, self.z + rhs.z )
      
   def __mul__( self, v ):
      return xyz( self.x * v, self.y * v, self.z * v )
      
   __rmul__ = __mul__      

   def __str__( self ):
      return( "[ %f, %f, %f ]" % ( self.x, self.y, self.z ) )  
      
   def __call__( self, rhs: element ):   
      return element_shift( self, rhs )      
      
def dup2( x ):
   return xy( x, x )

def dup3( x ):
   return xyz( x, x, x )   
   
def set_z( a, z ):
   return xyz( a.x, a.y, z )   


#============================================================================
# 
# elements: something that you can render in OpenScad
#
#============================================================================

class element:

   def __init__( self, parts = [] ):
      self._parts = parts
      
   def __iadd__( self, rhs: element ):
      self._parts.append( rhs )
      
   def __add__( self, rhs: element ):
      return element( self._parts + rhs )
      
   def __sub__( self, rhs: element ):
      return element_subtract( self, rhs )
      
   def __mul__( self, rhs: element ):
      return element_multiply( self, rhs )
      
   def _indent( self, txt: string ):
      return ssum( map(
         lambda s: "   " + s + "\n",
         txt.split( "\n" )
      ))   
           
   def __str__( self ):
      return ( 
         "union(){\n" + self._indent( ssum( map( 
            lambda x: str( x ) + "\n", 
            self._parts 
         ))) + "}" )
         
   def print( self, file_name ):
      f = open( file_name, "w" )
      f.write( str( self ) )
      f.close()

class element_subtract( element ):
         
   def __init__( self, a: element, b: element ):
      element.__init__( self )
      self.a, self.b = a, b
      
   def __str__( self ):
      return ( 
         "difference(){\n" +
            self._indent( str( self.a ) + "\n" + str( self.b ) + "\n" ) +
         "}" )
         
class element_multiply( element ):
         
   def __init__( self, a: element, b: element ):
      element.__init__( self )
      self.a, self.b = a, b
      
   def __str__( self ):
      return ( 
         "intersection(){\n" +
            self._indent( str( self.a ) + "\n" + str( self.b ) + "\n" ) +
         "}" )
         
class element_shift( element ):

   def __init__( self, direction : xyz, minion : element ):    
      element.__init__( self )
      self.minion = minion
      self.direction = direction

   def __str__( self ):      
      return ( 
         ( "translate( %s )\n" % str( self.direction ) ) +
            self._indent( str( self.minion ) )
      )
      
class element_extrude( element ):

   def __init__( self, z, minion : element ):    
      element.__init__( self )
      self.minion = minion
      self.z = z

   def __str__( self ):      
      return ( 
         ( "linear_extrude( %f )\n" % self.z ) +
            self._indent( str( self.minion ) )
      )
      
class element_rotate( element ):

   def __init__( self, d, minion : element ):    
      element.__init__( self )
      self.minion = minion
      self.d = d

   def __str__( self ):      
      return ( 
         ( "rotate( %s )\n" % str( self.d ) ) +
            self._indent( str( self.minion ) )
      )
      
      
#============================================================================
# 
# OpenScad shapes
#
#============================================================================

class primitive( element ):

   def __init__( self, text ):
      self.text = text
      
   def __str__( self ):
      return self.text     
      
class rectangle( primitive ): 

   def __init__( self, dimensions: xy ):
      primitive.__init__( self, 
         "square( %s );" % str( dimensions ))         
      
class box( primitive ): 

   def __init__( self, dimensions: xyz ):
      primitive.__init__( self, 
         "cube( %s );" % str( dimensions ))
      
class circle( primitive ): 

   def __init__( self, r, f = number_of_circle_facets ):
      primitive.__init__( self, 
          "circle( r=%f, $fn=%d );" % ( r, f ))          
     
class cylinder( primitive ): 

   def __init__( self, r, h, f = number_of_circle_facets ):
      primitive.__init__( self, 
          "cylinder( r=%f, h=%f, $fn=%d );" % ( r, h, f ))          
     
     
#============================================================================
# 
# element manipulators
#
#============================================================================     
     
class repeat4:

   def __init__( self, x, y ):
      self.x, self.y = x, y

   def __call__( self, rhs: element ):   
      return element( [
         xy(      0,      0 ) ** rhs,
         xy( self.x,      0 ) ** rhs,
         xy(      0, self.y ) ** rhs,
         xy( self.x, self.y ) ** rhs,
      ] )   
      
class extrude:

   def __init__( self, z ):
      self.z = z   
         
   def __call__( self, rhs: element ):   
      return element_extrude( self.z, rhs )
           
class rotate:

   def __init__( self, d ):
      self.d = d   
         
   def __call__( self, rhs: element ):   
      return element_rotate( self.d, rhs )
           
           
#============================================================================
# 
# derived shapes
#
#============================================================================     

def chisel( size ):
   return rectangle( size ) - dup2( size) ** circle( size )
      
def rounded_rectangle( size: xy, rounding ) -> element:
   ch = chisel( rounding )
   return rectangle( size ) - element( [
      ch,
      xy( 0, size.y ) ** rotate( 0, 0, -90 ) ** ch,
   ] )   
      
      
#============================================================================
# 
# 
#
#============================================================================     
      
      
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

      