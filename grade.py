percentage = float(input("Enter the percentage obtained in the exam: "))

if percentage >= 91 and percentage <= 100:
    grade = "A"
elif percentage >= 71 and percentage < 91:
    grade = "B"
elif percentage >= 60 and percentage < 71:
    grade = "C"
else:
    grade = "D"

print("Grade:", grade)
