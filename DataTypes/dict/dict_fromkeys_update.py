
tuple_1 = ('name', 'age','gender')
dict_1 = dict.fromkeys(tuple_1)
print(dict_1)
dict_2 = dict.fromkeys(tuple_1,'naresh')
print(dict_2)

student = {'name':'naresh', 'age':'27','subject':'math'}
employee = {'firstname':'madhu','oldage':'45','gender':'male'}
student.update(employee)
print(student)








