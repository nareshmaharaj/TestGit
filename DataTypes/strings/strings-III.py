
"""
rfind method :



"""

pyworld = "aws azure devops $$ and python"

print(pyworld, type(pyworld), id(pyworld), len(pyworld))

print(pyworld.find('azur',0,28))
print(pyworld.rfind('devops',0,28))

print(pyworld.rindex("azur"))
print(pyworld.index('devops'))
print(pyworld.split('$'))
print(pyworld.splitlines())
































