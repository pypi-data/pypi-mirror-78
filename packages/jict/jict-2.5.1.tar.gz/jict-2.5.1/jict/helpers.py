from time import time
from threading import Thread

def evaluate(foo, itter=1 , threaded = False ):

    if threaded == True:
        def threadedfoo():
            Thread(target = lambda: evaluate(foo,itter) ).start()

        threadedfoo()
        return

    t0 = time()
    for _ in range(itter):
        foo()
        
    print( time() - t0, "seconds wall time" )
