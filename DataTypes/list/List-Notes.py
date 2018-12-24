
num = [1, 2, 3, 4, 5, 6]
print(sum(num))

courses = ['physics', 'chem', 'math','history']
num = [1, 2, 3, 4, 5, 6]
print(courses[1])
print(num[2])

courses = ['physics', 'chem', 'math','history']
for course in courses:
    print(course)

courses = ['physics', 'chem', 'math','history']
for index, course in enumerate(courses,start=1):
    print(index,course)

courses = ['physics', 'chem', 'math','history']
course_str = ','.join(courses)
print(course_str)

courses = ['physics', 'chem', 'math','history']
course_str = '-'.join(courses)
print(course_str)

courses = ['physics', 'chem', 'math','history']
new_list = course_str.split('-')
print(new_list)

courses1 = ['physics', 'chem', 'math','history']
course2 = courses1
print(courses1)
print(course2)

courses1[0] = 'art'
print(courses1)
print(course2)













