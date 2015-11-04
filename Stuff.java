
public class Stuff {
    public int getSecondNum(){
	return 4;
    }
	public int getNum(){
		
	    return 2*this.getSecondNum();
	}
	public int doubleThis(int num){
		return 2*num;
	}
	public void printThing(){
		int num = this.getNum();
		getSecondNum();
		int doubled = OtherNum.doubleNum(num);
		int x;


		System.out.println("num: " + Integer.toString(doubled));
	}

}
