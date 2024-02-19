//Palindrome
package main
import "fmt"

func main() {
	var number,remainder,temp int
	var reverse int = 0

	fmt.Print("Enter a positive integer : ")
	fmt.Scan(&number)

	temp=number

	
	for{
		remainder = number%10
		reverse = reverse*10 + remainder
		number /= 10

		if(number==0){
			break 
		}
	}

	if(temp==reverse){
		fmt.Printf("%d is a Palindrome",temp)
	}else{
		fmt.Printf("%d is not a Palindrome",temp)
	}

}
	
/*
//reverse of string
func reverse(s string) string{
	r:=[]rune(s)
	for i,j:=0,len(r)-1;i<j;i,j=i+1,j-1{
		r[i], r[j] = r[j],r[i]
	}
	return string(r)
}
//check for palindrome
func isPalindrome(n int) string{
	s:=strconv.Itoa(n) 
	return s == reverse(s)
	if s == reverse(s) Printf("%d is palindrome")
	else Printf("%d is not palindrome")
}
*/
