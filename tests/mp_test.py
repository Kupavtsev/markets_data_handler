import time



def func_logic(asset, ses):
    print('Logic calc')
    print(asset, ses)
    time.sleep(1)
    return print('done')


def func_asset():
    assets = ['a','b','c']
    sessions = [1,2,3,4,5,]
    def func_sessions(asset):
        for ses in sessions:
            func_logic(asset, ses)

    for asset in assets:
        func_sessions(asset)

start = time.time()
func_asset()
end = time.time()
time_taken =  end - start
print(time_taken)   # 15
