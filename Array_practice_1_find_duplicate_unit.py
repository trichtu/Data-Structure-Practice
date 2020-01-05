
"""
    describe the question:
    only one element  in a array is duplicated, find the element
    requirement:
    each element is only be visited once, no extra memory space
"""
    
#Hash ---no satisfy 
def findDup(array):
    if array==None:
        print('array is empty.')
        return -1
    arrayhash = {}
    for i in range(len(array)):
        if i not in arrayhash.keys():
            arrayhash[array[i]] = 0
        else:
            return array[i]
    return -1

#accumulated summation
def findDup2(array):
    if array == None:
        print('array is empty.')
        return -1
    arraysum = 0
    for i in range(len(array)):
        arraysum += array[i]
    normal = 0
    for i in range(1,len(array)): #begin with 1, length - 1 + 1
        normal += i
    number = arraysum - normal
    return number

# XOR operator 
# i^ i =0 ; i^j =not 0
# (1^2^3^4^5)^(2^3^3^1^4^5) = (1^1)^(2^2)^(3^3^3)^(4^4)^(5^5)
def findDup3(array):
    if array==None:
        print('array is empty.')
        return -1
    result = 0
    for i in array:
        result ^= i
    for i in range(1,len(array)):
        result ^= i
    return result

#mappe from 0-1000 to 1-1000, circle,sign
def findDup4(array):
    if array==None:
        print('array is empty.')
        return -1 
    index = 0
    while True:
        value = array[index]
        array[index] = -value
        index = array[value]
        print(index , value)
        if index<0:
            break
        if index>=len(array):
            print('array value not normal')
            return -1 
    for i in array:
        if i>0:
            return i
    return -1     

if __name__ == "__main__":
    test_example = [1,3,4,2,5,3]
    print(findDup4(test_example))