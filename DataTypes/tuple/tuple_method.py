
tup1 = ("aws",'azure',1997,2947, 50.75)

tup2 = (1, 2, 3, 4, 5, 6, 7)

print(tuple(enumerate(tup1)),type(tup1),id(tup1),len(tup1))
print(tuple(enumerate(tup2)),type(tup2),id(tup2),len(tup2))

print(tup1[3])
print(tup1[:5])

print(tup1)

tup = (1,2, [1,3])
print(tuple(enumerate(tup)),type(tup))
print(tup,type(tup),tuple(enumerate(tup)))
print(tuple(enumerate(tup)),type(tup))


tup = (5, 6, [1,3])
print(tuple(enumerate(tup)),type(tup))

def hello_naresh():
   print('hello_naresh')
hello_naresh()

def naresh(x, y):
    s=x+y
    print(s)
naresh(20, 30)


naresh = '''welcome
to
sushmitha 
usa    
'''
print(naresh)

#list
c = [10, 3.56, "naresh"]
print(c)


#class Practice:
   # a = 50
    #print(a)
    #Practice.a
    #print(Practice.a)

def student_info(*args, **kwargs):
    print(args)
    print(kwargs)
courses = ['math', 'art']
info = {'name':'john','age':25}

student_info(*courses, **info)




















