union(){
   linear_extrude( 2.000000 )
      difference(){
         square( [ 84.000000, 89.000000 ] );
         union(){
            union(){
               union(){
                  translate( [ 0.000000, 0.000000 ] )
                     rotate( [ 0.000000, 0.000000, 0.000000 ] )
                        difference(){
                           square( 2 );
                           translate( [ 2.000000, 2.000000 ] )
                              circle( r=2.000000, $fn=32 );
                           
                           
                        }
                     
                  
                  translate( [ 0.000000, 89.000000 ] )
                     rotate( [ 0.000000, 0.000000, -90.000000 ] )
                        difference(){
                           square( 2 );
                           translate( [ 2.000000, 2.000000 ] )
                              circle( r=2.000000, $fn=32 );
                           
                           
                        }
                     
                  
                  
               }
               translate( [ 84.000000, 89.000000 ] )
                  rotate( [ 0.000000, 0.000000, -180.000000 ] )
                     difference(){
                        square( 2 );
                        translate( [ 2.000000, 2.000000 ] )
                           circle( r=2.000000, $fn=32 );
                        
                        
                     }
                  
               
               
            }
            translate( [ 84.000000, 0.000000 ] )
               rotate( [ 0.000000, 0.000000, -270.000000 ] )
                  difference(){
                     square( 2 );
                     translate( [ 2.000000, 2.000000 ] )
                        circle( r=2.000000, $fn=32 );
                     
                     
                  }
               
            
            
         }
         
      }
   
   translate( [ 7.000000, 6.000000 ] )
      union(){
         union(){
            union(){
               translate( [ 0.000000, 0.000000 ] )
                  difference(){
                     cylinder( r=4.000000, h=8.000000, $fn=32 );
                     cylinder( r=2.000000, h=8.000000, $fn=32 );
                     
                  }
               
               translate( [ 71.500000, 0.000000 ] )
                  difference(){
                     cylinder( r=4.000000, h=8.000000, $fn=32 );
                     cylinder( r=2.000000, h=8.000000, $fn=32 );
                     
                  }
               
               
            }
            translate( [ 0.000000, 73.500000 ] )
               difference(){
                  cylinder( r=4.000000, h=8.000000, $fn=32 );
                  cylinder( r=2.000000, h=8.000000, $fn=32 );
                  
               }
            
            
         }
         translate( [ 71.500000, 73.500000 ] )
            difference(){
               cylinder( r=4.000000, h=8.000000, $fn=32 );
               cylinder( r=2.000000, h=8.000000, $fn=32 );
               
            }
         
         
      }
   
   
}