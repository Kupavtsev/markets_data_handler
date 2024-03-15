
# import array

# a = array.array('i', [0]) * 2*9

hl_list = [[4,1],[7,3],[8,6],[5,2]]

# 1 2H
# h, l = 4, 1
period_ticks = [1,2,3,4,5,6,7,8]
periods_mp = [0]*len(period_ticks)

def mp_calc(hl):
    h = hl[0]
    l = hl[1]
    
    example      = [0,0,0,0,0,0,0,0]
    tick = 1

    for k in range(len(periods_mp)):
        # print(period_ticks[k])
        if period_ticks[k] in range(l, h+tick):
            # print(periods_mp[k])
            x = periods_mp[k]+1
            periods_mp[k] = x
            # print(periods_mp[k]+1)
            # periods_mp = [i+1 for i in periods_mp[k]+1]

    print(periods_mp)

def data_2h():
    hl_list = [[4,1],[7,3],[8,6],[5,2]]
    for hl in hl_list:
        mp_calc(hl)


data_2h()
print(periods_mp)