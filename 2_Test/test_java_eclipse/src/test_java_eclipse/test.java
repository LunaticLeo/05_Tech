package test_java_eclipse;

public class test {
    public static void main(String[] args) {
    	
    	Object a = "aaa";
    	System.out.println(a instanceof Object);
        System.out.println(new Object() instanceof Integer);
        // Incompatible conditional operand types String and ArrayList
    }
}