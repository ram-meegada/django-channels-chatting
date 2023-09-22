from celery import shared_task


# name = 'ram meegada'
# letters = set()
# for i,j in enumerate(name):
#     count = 1
#     if i == len(name)-1 and j not in letters:
#         print(f"count of {j} is:- ", 1)
#     elif i == len(name)-1 and j in letters:
#         break
#     if j not in letters:     
#         for k in name[i+1:]:
#             if j == k:
#                 count += 1
#         letters.add(j)
#         print(f"count of {j} is:- ",count)


# dictionary = {'ram':1, 'vikhil':2, "indrajeet":3}
# print(dictionary.items())

# name = "indrajeet"
# string_reverse = name[::-1]
# print(string_reverse)
# reverse_string = ''
# for character in range(len(name)-1, -1, -1):
#     reverse_string += name[character]
# print(reverse_string)   


# hex_value = "0000020371346430"
# integer_value = 0
# for i in hex_value:
#     integer_value += 10*(16**int(i))
# print(integer_value)    


# records = 'ram moj vikhil jnasd yfyt uyby'
# print(records.split())

# string = ''.join(2)
# print(string)

# alice = [17,28,30]
# bob = [99,16,8]
# result = [0,0]

# for i in range(0,len(alice)):
#     if alice[i] > bob[i]:
#         result[0] = result[0] + 1
#     elif alice[i] < bob[i]:
#         result[1] = result[1] + 1
#     elif alice[i] == bob[i]:
#         pass
# print(result)    

# matrix = [[11,2,4], [4,5,6], [10,8,-12]]
# diagnal1 = 0
# diagnal2 = 0
# for i in range(0, len(matrix)):
#     diagnal1 += matrix[i][i]
#     diagnal2 += matrix[i][len(matrix)-i-1]
# print(abs(diagnal1-diagnal2))    

# a,b,c = 12, 5, 45
# if a<b and a<c:
#     print(a)
# elif b<a and b<c:
#     print(b)    


# lst = [1,2,3] + [4]
# print(lst)
# lst2 = [1,2,3]
# lst1 = [4,5]
# print(list(zip(lst1,lst2)))

# lst = [1,2,3]
# new_lst = lst
# new_lst[1] = 10
# print(lst, id(lst))
# print(new_lst, id(new_lst))
import base64
import random

# random_password = base64.b64encode(str(random.randint(1000000,9999999)).encode()).decode()
# print(random_password)
# a = [(1,2), (4,5), (2,1), (4,1)]

# def answer(nums):
#     res = {}
#     for i in range(len(nums)):
#         for j in range(len(nums)):
#             if j == i:
#                 continue
#             else:
#                 for k in range(len(nums)):
#                     if k in [i, j]:
#                         continue
#                     else:
#                         if (nums[i] + nums[j] + nums[k]) == 0:
#                             add = [nums[i],nums[j],nums[k]]
#                             add.sort()
#                             res[i] = add
#     return list(res.values())


# def answer2(nums):
#     store = set(nums)
#     for i in range(len(nums)):
#         for j in range(len(nums)):
#             if -1*(nums[i] + nums[i+1]) in store and :
#                 print(nums[i], nums[i+1], -1*(nums[i] + nums[i+1]))


# nums = [-1,6,1,7,0,-4]
# print(answer2(nums))

# dis = {3:1, 1:3, 2:2}
# sorted_dis = {i:j for i,j in sorted(dis.items(), key=lambda v:v[1])}
# print(sorted_dis)
# lst = [1,2,3,4]
# print(id(lst))
# lst.remove(2)
# print(lst, id(lst))
# lst.insert(0,10)
# print(lst, id(lst))

# a = {12,3,4}
# for i in a:
#     print(i)
s = [1,2,3,4]
a = set(s)
t = (1,2)
d = {1:2, 2:2}
# print(hash(s))
# s = "abc"
# permutations = []
# for i in range(0,3):
#     for j in range(2):
#         pass

# def answer(nums):
#     res = 0
#     for i in range(0, len(nums)):
#         lst = [nums[i]]
#         for j in range(i+1, len(nums)):
#             if nums[j] > lst[-1]:
#                 lst.append(nums[j])
#         print(lst)        
#         if len(lst)>res:
#             res = len(lst)
#     return res 
# nums = [0,1,0,3,2,3]
# lst = nums[:]
# lst.sort()
# lst = list(set(lst))
# print(lst, nums)
# print(answer(nums))
# lst = [1,2,3,17,10]
# lst.sort()
# cost = 0
# i = 0
# while i < len(lst):
#     cost += 1
#     if 
# input = input()
# print(input)
lst1 = [1,2,3]
lst2 = [4,5]
# print(list(zip(lst1, lst2)))
# def ans():
#     return
# print(ans())
import base64

def create_apikey():
    api_key = base64.b64encode(str(random.randint(10000000000, 99999999999)).encode()).decode()
    return api_key
x = create_apikey()

api_key_field = f'{create_apikey()}:{create_apikey()}'
production_key = api_key_field.split(':')[0]    
sandbox_key = api_key_field.split(':')[1]    

print('api_key_field',api_key_field,'\n', production_key, '\n',sandbox_key)    
# message=xml_payload['{http://tempuri.org/}msg1'],
#                                                      messageType=xml_payload['{http://tempuri.org/}ERX001'],
#                                                      conversationId=xml_payload['{http://tempuri.org/}2HTWKVQHXG5PR524D5'],
#                                                      entityId=xml_payload['{http://tempuri.org/}HTWKV'],
#                                                      destinationId=xml_payload['{http://tempuri.org/}00000']
import json
d = {'a':1, 'b':2}
encoded_string = json.dumps(d).encode('utf-8')
print(encoded_string, type(encoded_string))