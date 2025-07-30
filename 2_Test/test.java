// java test.java

import java.util.*;
import java.util.stream.*;

public class test 
{
    
    public static void main( String[] args )
    {   
    
        String str = "Welcome to Pax.";

        String[] a = str.split(" ");

        int i =0, j = a.length;

        

        while(i<j){
            string temp = a[i];
            a[i] = a[j];
            a[j] = a[i];  
        }

        String output = "";

        for(int i= 0;i<a.length;i++){
            output.concat(a[i]);
        }

        System.out.println(output);

    }

   
}
 