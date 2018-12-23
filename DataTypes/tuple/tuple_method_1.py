
tup1 = ("aws",'azur',1988,2050,50,57)
tup2 = (1,2,3,4,5,6,7)

print(tuple(enumerate(tup1)),type(tup1),id(tup1),len(tup1))
print(tuple(enumerate(tup2)),type(tup2),id(tup2),len(tup2))

print(tup1[3:])
print(tup1[-3])
print(tup2[:4])
print(tup2[0:])
#del(tup1[0]) #tuple object doesnot support item deletion

tup = (1,2,[1,2])
print(tuple(enumerate(tup)),type(tup))



















