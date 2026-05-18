#多进程编程代码演示

from multiprocessing import Process  
import os

def targe_function():
    print(f'子进程开始，id为{os.getpid()}')

if __name__ == '__main__':
    print('主进程开始',__name__)
    print(f'主进程id{os.getpid()}')
    ps=[]
    for i in range(10):
        p = Process(target=targe_function)
        p.start()
        ps.append(p)
    
    #让主进程等待子进程运行完成后再停止
    for p in ps:
        p.join()
    print('主进程结束')