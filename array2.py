words=[]
n=int(input("Number of words in array:"))
for i in range(0,n):
   l=str(input())
   words.append(l)
print(words)

for word in words:
    for letter in word:
        print(letter) 

