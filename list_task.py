def remove_adjacent(lst):
    if len(lst) == 0:
        return lst
    
    stack = [lst[0]]
    for i in range(len(lst)):
        if stack[-1] != lst[i]:
            stack.append(lst[i])
    return stack
def linear_merge(lst1, lst2):
    ans = []
    i, j = 0, 0
    
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            ans.append(lst1[i])
            i = i + 1
        else:
            ans.append(lst2[j])
            j = j + 1
            
    while i < len(lst1):
        ans.append(lst1[i])
        i = i + 1
        
    while j < len(lst2):
        ans.append(lst2[j])
        j = j + 1
    return ans
