package test_java_eclipse;

import java.util.*;

public class test {

	public static int solution(int[] nums) {

		Map<Integer, Integer> map = new HashMap<>();
	    int max = 0;

	    for (int num : nums) {
	        if (!map.containsKey(num)) {
	            int left = map.getOrDefault(num - 1, 0);
	            int right = map.getOrDefault(num + 1, 0);

	            int sum = left + 1 + right;

	            map.put(num, sum);
	            max = Math.max(max, sum);
	            
	            map.put(num - left, sum);
	            map.put(num + right, sum);
	        }
	    }
	    System.out.println(max);
	    return max;
	}

	public static void main(String[] args) {

		solution(new int[] { 100, 4, 200, 1, 3, 2 });
		solution(new int[] { -1, 0, 1, 2, -1, -4 });
		solution(new int[] { 0, 1, 1 });
	}
}
