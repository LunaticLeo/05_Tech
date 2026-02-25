package test_java_eclipse;

import java.util.*;

public class test {

	public static int solution(int[] nums) {

		return null;

	}

	public static void main(String[] args) {

//		solution(new int[] { 100, 4, 200, 1, 3, 2 });
//		solution(new int[] { -1, 0, 1, 2, -1, -4 });
//		solution(new int[] { 0, 1, 1 });
		
		ArrayList<Integer> a = new ArrayList<>(List.of(1,2,3));
		
		a.addAll(1,List.of(4));
		
		System.out.print(a);
		
	}
}
