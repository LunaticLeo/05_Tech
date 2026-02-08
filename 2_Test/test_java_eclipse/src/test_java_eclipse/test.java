package test_java_eclipse;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.function.Function;

public class test {
	
	public static List<List<Integer>> solution(int[] nums){
		
		HashMap<Integer, HashSet<String>> hm = new HashMap<>();
		
		for(int i=0;i<nums.length;i++) {
			for(int j=i+1;j<nums.length;j++) {
				HashSet<String> temp = hm.getOrDefault(nums[i]+nums[j], new HashSet<String>());
				if(nums[i]<nums[j]) {
					temp.add(""+nums[i]+","+nums[j]);
				}else {
					temp.add(""+nums[j]+","+nums[i]);
				}
				hm.put(nums[i]+nums[j], temp);
			}
		}
				
		HashSet<Integer> numsUnique = new HashSet<>();
		List<List<Integer>> output = new ArrayList<>();
		
		for(int i=0;i<nums.length;i++) {
			if(numsUnique.contains(nums[i]) == false) {
				numsUnique.add(nums[i]);
				if(hm.containsKey(0-nums[i])) {
					HashSet<String> temp = hm.get(0-nums[i]);
										
					for(String s: temp) {
						ArrayList<Integer> temp2 = new ArrayList<Integer>();
						String[] parts = s.split(",");
						temp2.add(nums[i]);
						temp2.add(Integer.parseInt(parts[0]));
						temp2.add(Integer.parseInt(parts[1]));
						output.add(temp2);
					}
					
				}
			}
		}
		
		System.out.println(output);
		
		return output;
	}
	
    
    public static void main(String[] args) {
    	
    	solution(new int[] {0,0,0});
    	solution(new int[] {-1,0,1,2,-1,-4});
    	solution(new int[] {0,1,1});

    }
}