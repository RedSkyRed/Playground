# def best_revenue(revenue, travel_days, start):
#     # What do if travel days is empty?
#     max_days = len(revenue)
#     max_cities = len(revenue[-1])
#     profit = [float('-inf')] * max_cities
#     profit[start] = 0
#     previous_days_profit = []

#     # Days loop
#     for d in range(0,max_days):
#         # Daily update
#         # Update each city that has been visited with the revenue that they would make staying at the city.
#         previous_days_profit.append(profit.copy())   
#         for x in range(max_cities):
#             if profit[x] != float('inf'):
#                 profit[x] += revenue[d][x]
#         # Bellman loop
#         bellman_ford(travel_days, profit, d, max_cities, previous_days_profit)
        

#     # Max value after doing bellmans
#     max_revenue = find_max(profit)
#     return max_revenue


# def bellman_ford(travel_days, profit, day, max_cities, previous_d_profit):
#     changes = True
#     for i in range(max_cities-1):
#         if changes == False:
#             break
#         else:
#             changes = False
#         for x in range(len(profit)):
#             if profit[x] != float('-inf') and profit[x] != 0:
#                 for y in range(len(travel_days[x])):
#                     route_length = travel_days[x][y]
#                     if route_length <= day + 1 and route_length != -1:
#                         if profit[y] == float('-inf'):
#                             profit[y] = 0
#                         elif previous_d_profit[day+1-route_length][x] > profit[y]:
#                             profit[y] = previous_d_profit[day+1-route_length][x]
                    

# def find_max(arry):
#     max_value = arry[0]
#     for i in range(1,len(arry)):
#         if arry[i] > max_value:
#             max_value = arry[i]
#     return max_value




# # Testing

# #       city:    0  1  2  3   # city:
# travel_days = [[-1,-1, 3, 1], # 0
#                 [-1,-1,-1, 1], # 1
#                 [ 1,-1,-1, 1], # 2
#                 [ 1, 1, 2,-1]] # 3

# #       city:    0     1  2  3 # day:
# revenue =     [[ 1,    2, 3, 4], # 0
#                 [ 3,    6, 1, 5], # 1
#                 [ 1,    8, 4, 1], # 2
#                 [ 1,   10, 4, 5], # 3
#                 [10,    4, 5, 9]] # 4
# start = 3

# print(best_revenue(revenue, travel_days, start))