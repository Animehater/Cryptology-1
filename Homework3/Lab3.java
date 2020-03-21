import java.io.*;

public class Lab3{
	public static boolean advGame(){
		return True;
	}
	public static void testAdv(){
		int numTrue = 0;
		int numTries = 3000;
		try(FileReader reader1 = new FileReader("ecb-distinguish-1.txt")){
			char c = reader1.read();
		}
		catch(IOException){
			System.out.println(ex.getMessage());
		}

		try(FileReader reader2 = new FileReader("ecb-distinguish-2.txt")){
			char c = reader2.read();
		}
		catch(IOException){
			System.out.println(ex.getMessage());
		}

		for(int i=0; i<numTries; i++){
			if (advGame()){
				numTrue++;
			}
		}
		double ratio = numTrue / numTries;
		System.out.println(ratio);

	}

	public static void main (String[] args) {
		testAdv();
	}
}