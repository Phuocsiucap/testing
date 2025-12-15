class Arrays
{
    String [] arrayA= {
            "dragon"
    };
    String [] arrayB= {
            "dog", "dog", "cat","dog","frog","rat","turtle",
            "fox","fox","man","man","frog","man"
    };

    public void compare()
    {
        for (int indexA =0; indexA<arrayA.length;indexA++){
            int counter =0;
            for(int indexB=0; indexB<arrayB.length;indexB++){
                if(arrayA[indexA] == arrayB[indexB]){
                    counter++;
                }
            }// end for

            if(counter > 0){
                System.out.println(arrayA[indexA] + "  " + counter);
            }
        }// end for
    }//end compare()

    public static void main(String args[]){
        Arrays a = new Arrays();
        a.compare();
    }
}// end class Arrays
