
coollist = ["naresh","mahesh",5555,99999,"madhu"]
morelist = [44, 55, 66, 77, 88, 99]

coollist.pop()
morelist.pop()
print(coollist,list(enumerate(coollist)))
print(morelist,list(enumerate(morelist)))
coollist.pop(2)
morelist.pop(4)
print(coollist,list(enumerate(coollist)))
print(morelist,list(enumerate(morelist)))


coollist = ["naresh","mahesh",5555,99999,"madhu"]
morelist = [44, 55, 66, 77, 88, 99]

coollist.remove("mahesh")
morelist.remove(66)
print(coollist,list(enumerate(coollist)))
print(morelist,list(enumerate(morelist)))


coollist = ["naresh","mahesh",5555,99999,"madhu"]
morelist = [44, 55, 66, 77, 88, 99]
print(coollist.index("madhu"))
print(morelist.index(99))

nums = [44, 55, 66, 77, 88, 99]

for num in nums:
    print(num)

for index,num in enumerate(nums,start=1):
    print(index,num)

coollist = ["naresh","mahesh","madhu"]
morelist = [44, 55, 66, 77, 88, 99]

coollist_str = ','.join(coollist)

print(coollist_str)

coollist = ["naresh","mahesh","madhu"]

new_coollist = coollist_str.split("-")
print(new_coollist)

coollist1 = ["naresh","mahesh","madhu"]
coollist2 = coollist1
print(coollist1)
print(coollist2)
coollist1[0]= "art"
print(coollist1)
print(coollist2)

coollist = ['abc','xyz','b','d']
morelist = [8,9,5,3,7,2,10]

print(min(coollist))
print(max(morelist))

dic1 = {'name':'naresh','age':'28','courses':'ms'}
print(dic1,type(dic1),id(dic1),len(dic1),dict(enumerate(dic1)))

dic1 = {'name':'naresh','age':'28','courses':'ms'}
dic1['age'] = 28
print(dic1)
dic1['courses'] = 'math'
print(dic1)

print(dic1['age'])
print(dic1)























