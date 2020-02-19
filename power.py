from __future__ import annotations
from functools import reduce

number_of_facets = 32

def ssum( x ):
   return "".join( x )

class xy:

   def __init__( self, x, y ):
      self.x, self.y = x, y
   
   def __add__( self, rhs: xy ):
      return xy( self.x + rhs.x, self.y + rhs.y )
      
   def __mul__( self, v ):
      return xy( self.x * v, self.y * v )
      
   def __str__( self ):
      return( "[ %f, %f ]" % ( self.x, self.y ) )  
      
   def __call__( self, rhs: element ):   
      return element_shift( xyz( self.x, self.y, 0 ), rhs )            

class xyz:

   def __init__( self, x, y, z ):
      self.x, self.y, self.z = x, y, z
   
   def __add__( self, rhs: xyz ):
      return xyz( self.x + rhs.x, self.y + rhs.y, self.z + rhs.z )
      
   def __mul__( self, v ):
      return xyz( self.x * v, self.y * v, self.z * v )

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

class element:

   def __init__( self, parts = [] ):
      self._parts = parts
      
   def __iadd__( self, rhs: element ):
      self._parts.append( rhs )
      
   def __add__( self, rhs: element ):
      return element( self._parts + rhs )
      
   def __sub__( self, rhs: element ):
      return element_subtract( self, rhs )
      
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
 
class rectangle( element ): 

   def __init__( self, dimensions: xyz ):
      element.__init__( self )
      self.dimensions = dimensions
      
   def __str__( self ):
      return "cube( %s );" % str( self.dimensions )
      
class cylinder( element ): 

   def __init__( self, r, h, f = number_of_facets ):
      element.__init__( self )
      self.r = r
      self.h = h
      self.f = f
      
   def __str__( self ):
     return "cylinder( r=%f, h=%f, $fn=%d );" % ( self.r, self.h, self.f )
     
class repeat4:

   def __init__( self, x, y ):
      self.x, self.y = x, y

   def __call__( self, rhs: element ):   
      return element( [
         xy(      0,      0 ) ( rhs ),
         xy( self.x,      0 ) ( rhs ),
         xy(      0, self.y ) ( rhs ),
         xy( self.x, self.y ) ( rhs ),
      ] )   
         
      
c = repeat4( 10, 30 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
cx = xy( 0, 0 ) ( cylinder( 5, 15 ) - cylinder( 2, 15 ) )
c.print( "f.scad" )
      

pcb = xy( 78, 83 )
margin = 1
wall = 1
plate = pcb + dup2( margin ) * 2 + dup2( wall ) * 2
bottom = rectangle( set_z( plate, wall ))
bottom.print( "f.scad" )

      