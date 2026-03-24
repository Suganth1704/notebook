from typing import List, Dict
#from typeguard import typechecked
# Fibonacci Series
def getFib(n):
    fib = [0,1]
    if n == 0:
        print(f"fib series: {n}")
    else:
        for i in range(n):
            fib.append(fib[-1]+fib[-2])
    return fib

def fatorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

#@typechecked
def getMaxInList(l:List[int]) -> int:
    print(type(l)) #max()
    max:int = 0
    for i in l:
        if i > max:
            max = i
    return max

#@typechecked
def getMinInList(l:List[int]) -> int:
    print(type(l)) #max()
    min:int = l[0]
    for i in l:
        if i < min:
            min = i
    return min

#rev string
#@typechecked
def reverseStr(s:str) -> str:
    #return s[::-1]
    #return "".join(list(reversed(list(s))))
    '''
    rev = ""
    for i in s:
        rev = i + rev
    return rev
    '''
    string = list(s)
    st = 0
    e = len(string)-1
    while st < e:
        # temp = string[st]
        # string[st] = string[e]
        # string[e] = temp
        string[st],string[e] = string[e],string[st]

        st +=1
        e -=1
        print(string)
    return "".join(string)


def twoSum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        comp = target - num
        if comp in num_map:
            return [num_map[comp], i]
        num_map[num] = i
        print(num_map)
    return []


def revList(li:list):
    st = 0
    e=len(li)-1
    while st <e:
        li[st],li[e]=li[e],li[st]

        st +=1
        e-=1
    return li

def bubble_sort(arr:list):
    n=len(arr)
    for i in range(n):
        for j in range(0,n-i-1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
    return arr


if __name__ == "__main__":
    # print(f"Max : {getMaxInList([1,2,3,77,5,6])}")
    # print(f"Min : {getMinInList([1,2,3,77,5,6,0])}")
    #print(f"Rev str: {reverseStr('Suganth')}")
    #print(f"two sum: {twoSum([2, 7, 11, 15],13)}")
    # print(f"Rev List : {revList(li=[1,2,3,4,5])}")
    print(f"Rev list : {bubble_sort(arr=[2,6,5,4,7])}")




    