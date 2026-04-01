def sum_index(arr:list, n:int):
    l = list(enumerate(arr))
    for i in range(len(l)):
        s = l[i][1]
        for j in l:
            if j[1] ==s:
                pass
            else:
                if s+j[1] == n:
                    return (l[i][0],j[0])

from collections import deque

def odd_even(odd:int, even:int, limit:int):
    final_list = []
    arr = list(range(1,limit+1))
    even_queue = deque(list(filter(lambda x: x%2 == 0, arr)))
    odd_queue = deque(list(filter(lambda x: x%2 != 0, arr)))

    while True:

        if len(odd_queue) == 0  and len(even_queue) == 0:
            break

        for _ in range(odd):
            if len(odd_queue) != 0:
                final_list.append(odd_queue.popleft())
            else:
                pass
        
        for _ in range(even):
            if len(even_queue) != 0:
                final_list.append(even_queue.popleft())
            else:
                pass
    
    return final_list

if __name__ == "__main__":
    # arr = list(range(1,18))
    # arr = [1,2,5,8,10,12,13,19,3]
    # ind=sum_index(arr=arr, n=5)
    # print(ind)
    odd_even_list = odd_even(odd=4, even=3, limit=100)
    print(odd_even_list)
        

        