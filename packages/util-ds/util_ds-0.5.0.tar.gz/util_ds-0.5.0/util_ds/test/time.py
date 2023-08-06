import time

def testtime(func):
    num = 0 

    def call_fun(*args, **kwargs):
        nonlocal num 
        start = time.time()  
        num += 1 
        func(*args, **kwargs)
        end = time.time() 
        longtime = end - start
        print("Function: {}, The counted {}, the time {}".format(func, num, longtime))

    return call_fun