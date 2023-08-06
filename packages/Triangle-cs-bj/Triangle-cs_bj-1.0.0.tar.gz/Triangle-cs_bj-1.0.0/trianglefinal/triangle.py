'''DocString
Module Name: triangle
Module built to
    1)compute area by passing (base,height)as params
    2)compute area by passing (side1,side2,side3)as param
    3)compute peimeter
    4)check if a given triangle is right angled
    5)Check the type of the triangle if it exists
@end DocString
'''
def tArea(base,height):
    return (1/2)*base*height
def theron(*argv):
    if tcheck(*argv)==True:                                                            #argv is a variable to accept args
        assert len(argv)==3,"The args provided should be only 3"  # It is vital to check the input value (here using assert as assert return None if True
                                                                #,return AssertionError  if False Thereby Nullifying Use of if conditionals        
        s=tperim(*argv)/2                                            #semiperimeter is implicitly used as function by itself rather than explicitly declaring stuff again!!
        a=(arg for arg in argv)                                     #a here is a generator Object (for eg range())can be accesed using either for loop or next()
        return (s*(s-next(a))*(s-next(a))*(s-next(a)))**0.5         #if a has a=(a,b,c) next(a)first is a then b then c
    else:
        return "Invalid Sides"
def tperim(*argv):
    if tcheck(*argv)==True:
        if len(argv)==3:
            return (sum(argv))
        else:
            raise ValueError ("There Must Be 3 arguements")        #Raising Exceptions
    else:
        return "Invalid Sides"
def tright(*argv):
    if tcheck(*argv)==True:
        assert len(argv)==3,"The args provided should be only 3"
        l3=[]
        l3+=[arg for arg in argv]
        l3.sort(reverse=True)
        if l3[0]**2==l3[1]**2+l3[-1]**2:                                 #Instead of checking each sides i have sorted the list in reverse so the largest first then two 
            return True                                                  #smallest so it is obvious 
        else:
            return False
    else:
        return "Invalid Sides"

def ttype(*argv):
    if tcheck(*argv)==True:
        assert len(argv)==3,"The args provided should be only 3"

        if argv[0]==argv[1]==argv[-1]:
            return "Equilateral Triangle"
        elif (argv.count(argv[0]))>1 or argv.count(argv[1])>1 or argv.count(argv[-1])>1:#check count >1 if duplicate then isoceles if 3 duplicates then mov to condition1
            return "Isoceles Triangle"

        elif (argv.count(argv[0]))==1 or argv.count(argv[1])==1 or argv.count(argv[-1])==1:#same stuff
            if tright(*argv)==True:
                return "Right Triangle"
            else:
                return "Scalene Triangle"
    else:
        return "Invalid Sides"
def tcheck(*argv):
    if argv[0]+argv[1]>=argv[-1] and argv[1]+argv[-1]>=argv[0] and argv[-1]+argv[0]>=argv[1]:
        return True
    else:
        return False
        
    













