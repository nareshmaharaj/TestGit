student1 = {'name':'naresh', 'age':'27','subject':'math'}
student1['name'] = 'madhu'
print(student1)

tuple_1 = ('name', 'age','gender')
dict_1 = dict.fromkeys(tuple_1)
dict_1['name'] = 'naresh'
dict_1['age'] = '23'
dict_1['gender'] = 'male'
print(dict_1)

tuple_1 = ('name', 'age','gender')
dict_1 = dict.fromkeys(tuple_1)
dict_2 = dict.fromkeys(tuple_1,'naresh')
dict_1['name'] = 'naresh'
dict_1['age'] = '23'
dict_1['gender'] = 'male'
print(dict_1)
print(dict_2)
print(dict_1)


