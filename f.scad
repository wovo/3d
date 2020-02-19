difference(){
   square( [ 10.000000, 5.000000 ] );
   union(){
      difference(){
         square( 2 );
         translate( [ 2.000000, 2.000000, 0.000000 ] )
            circle( r=2.000000, $fn=32 );
         
         
      }
      translate( [ 0.000000, 5.000000, 0.000000 ] )
         difference(){
            square( 2 );
            translate( [ 2.000000, 2.000000, 0.000000 ] )
               circle( r=2.000000, $fn=32 );
            
            
         }
      
      
   }
   
}