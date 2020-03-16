
public class Lab2{
	public static long enc(long key, long message){
		return key*message;
	}

	public static long[] adv1(){
		long[] buff = new long[]{0,1};
		return buff;
	}

	public static int adv2(long cipher){
		if (cipher == 0){
			return 0;
		}
		else{
			return 1;
		}
	}

	public static boolean indotcpaGame(){
		long size = (long)Math.pow(2,32);
		int bit = (int)(Math.random()*2);
		long key = (int)(Math.random()*size);
		long message[] = new long[2];
		while(true){
			message = adv1();
			if (0>message[0] || message[0]>size || 0>message[1] || message[1]>size){
				System.out.println("Wrong size of messages");
			}
			else break;
		}	
		long cipher = enc(key,message[bit]);
		int bit2 = adv2(cipher);
		if(bit2 == bit){
			return true;
		}
		return false;
	}
	public static void test_indotcpa(){
		int numTrue = 0;
		int numTries = 10000000;
		for(int i=0; i<numTries; i++){
			if (indotcpaGame()){
				numTrue++;
			}
		}
		float ratio = numTrue/numTries;
		System.out.println(ratio);
	}

	public static void main (String[] args) {
		test_indotcpa();
	}
}
