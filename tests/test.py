
# import array
import numpy as np

# a = array.array('i', [0]) * 2*9


# 1 2H
# h, l = 4, 1
period_ticks = [ 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8 ]
periods_mp   = [0]*len(period_ticks)
example      = [0,0,0,0,0,0,0,0]
def mp_calc(hl):
    h = hl[0]
    l = hl[1]
    tick = 1.1
    for k in range(len(periods_mp)):
        # if l >= period_ticks[k] and period_ticks[k] <= h:
        if period_ticks[k] >= l and period_ticks[k] <= h:
            # print(period_ticks[k])
            periods_mp[k] = periods_mp[k]+1
        # elif l >= period_ticks[k] and period_ticks[k] <= h:
            # print(period_ticks[k])
            # periods_mp[k] = periods_mp[k]+1
    print(periods_mp)
def data_2h():
    # hl_list = [[4,1], [7,3], [8,6], [5,2]]
    hl_list = [[5.4, 2.2]]
    for hl in hl_list:
        mp_calc(hl)
data_2h()
# print(periods_mp)



# Working version with Integers
# period_ticks = [1.1,2.2,3,4,5,6,7,8.1]
# periods_mp = [0]*len(period_ticks)

# def mp_calc(hl):
#     h = hl[0]
#     l = hl[1]
    
#     example      = [0,0,0,0,0,0,0,0]
#     tick = 1

#     for k in range(len(periods_mp)):
#         # print(period_ticks[k])
#         if period_ticks[k] in range(l, h+tick):
#             # print(periods_mp[k])
#             x = periods_mp[k]+1
#             periods_mp[k] = x
#             # print(periods_mp[k]+1)
#             # periods_mp = [i+1 for i in periods_mp[k]+1]

#     print(periods_mp)

# def data_2h():
#     hl_list = [[4,1],[7,3],[8,6],[5,2]]
#     for hl in hl_list:
#         mp_calc(hl)


# data_2h()
# print(periods_mp)