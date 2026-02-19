package test_java_eclipse;

public class test {		
	
	public static int solution(int[] input, int kth) {
			
		int point = input.length/2;
		
		while(point == kth) {
			int a = 0, b = input.length-1;
			for(int i =0; i<input.length;i++) {
				if(i != point) {
					if(input[i]>input[point]) {
						
					}
				}
			}
		}
		
		return 0;
	}
    
    public static void main(String[] args) {
    	
    	
    }
}