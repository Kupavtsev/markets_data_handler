
import numpy as np


class MarketProfile():
    period_in_ticks = [ 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8 ]
    periods_mp   = [0]*len(period_in_ticks)
    # example      = [0,0,0,0,0,0,0,0]
    def mp_calc(self, hl):
        h = hl[0]
        l = hl[1]
        tick = 1.1
        for k in range(len(self.periods_mp)):
            if self.period_in_ticks[k] >= l and self.period_in_ticks[k] <= h:
                self.periods_mp[k] = self.periods_mp[k]+1
        # print(periods_mp)
    def data_2h(self):
        hl_list = [[4.4,1.1], [7.7,3.3], [8.9,6.6], [5.5,0.9]]
        for hl in hl_list:
            self.mp_calc(hl)




# 1 2H
def master():
    period_in_ticks = [ 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8 ]
    periods_mp   = [0]*len(period_in_ticks)
    # example      = [0,0,0,0,0,0,0,0]
    def mp_calc(hl):
        h = hl[0]
        l = hl[1]
        tick = 1.1
        for k in range(len(periods_mp)):
            if period_in_ticks[k] >= l and period_in_ticks[k] <= h:
                periods_mp[k] = periods_mp[k]+1
        # print(periods_mp)
    def data_2h():
        hl_list = [[4.4,1.1], [7.7,3.3], [8.9,6.6], [5.5,0.9]]
        for hl in hl_list:
            mp_calc(hl)
    data_2h()
    print(periods_mp)

master()



# Working version with Integers
# period_in_ticks = [1.1,2.2,3,4,5,6,7,8.1]
# periods_mp = [0]*len(period_in_ticks)

# def mp_calc(hl):
#     h = hl[0]
#     l = hl[1]
    
#     example      = [0,0,0,0,0,0,0,0]
#     tick = 1

#     for k in range(len(periods_mp)):
#         # print(period_in_ticks[k])
#         if period_in_ticks[k] in range(l, h+tick):
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