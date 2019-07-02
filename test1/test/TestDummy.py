#!python2

import multiprocessing
import subprocess

def func(objArgument, objResultQueue):
    print("Test",objArgument)
    objResultQueue.put( objArgument )
    assert False

def main():
    objArguments = [0,1,2]
    objResultQueue = multiprocessing.Queue()
    for intIndex in objArguments:    
        #multiprocessing.Process \
        #    ( target = func
        #    , args = ( objArguments[intIndex], objResultQueue )
        #    ).start()
        subprocess.call(__file__, shell=True)
    
    #for intIndex in range(3):
    #    objGenData = objResultQueue.get()
    #    print(objGenData)


if __name__ == "__main__" :
    main()
