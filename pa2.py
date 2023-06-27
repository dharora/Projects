def is_palindrome(word):
    
    # Convert the word to lowercase and remove any whitespace
    word = word.lower().replace(" ", "")

    # Check if the reversed word is equal to the original word
    if word == word[::-1]:
        return True
    else:
        return False

# Test the function
input_word = input("Enter a word: ")
if is_palindrome(input_word):
    print("The word is a palindrome.")
else:
    print("The word is not a palindrome.")
