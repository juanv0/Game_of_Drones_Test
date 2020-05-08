"""
Function to implement the matricial cross product wich is used to give te result
of scissor (s) vs rock (r) vs paper (p), it work like this:
s vs p = r vs s = p vs r = 1, this means the first element wins the round
p vs s = s vs r = r vs p = -1, this means the last element wins the round 
Note: I assume that each element is a orthogonal vector in 3-dimension as
s = [1,0,0], p = [0,1,0], r = [0,0,1] so the cross´product give this result,
further reading about cross product could be found at any linear algebra book
"""


# This function expects two 3D vector of s,r,p vector representation mentioned
def first_wins(v1, v2):
    
    # this is the implementation of matricial cross product
    a = (v1[1]*v2[2])-(v2[1]*v1[2])
    b = (v2[0]*v1[2])-(v1[0]*v2[2])
    c = (v1[0]*v2[1])-(v2[0]*v1[1])
    res = [a, b, c]
    # becouse orthonormality | a + b + c | = 1
    sign = a + b + c
    return sign
    # if sign == 0:
        # print("Draw-----")
        
    # # I use the sign to decide what player win
    # if sign < 0:
        # return False
    # return True


