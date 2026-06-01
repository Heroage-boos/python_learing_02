import  threading
import time

def worker():
    print('i am thread')
    t = threading.current_thread()
    time.sleep(10)
    print(t.getName())

# 子线程会在主线程之后执行 和 主线程共享资源
new_t = threading.Thread(target=worker)
new_t.start()

t= threading.current_thread();
print(t.getName()) # MainThread

''' 多线程的优缺点
更加充分的利用CPU的性能优势
异步编程
单核CPU
4核 a核  b核 并行的执行程序

Python 没办法充分利用多核优势  --> 异步编程

如何看待python的多线程是鸡肋?
GIL 全局解释器锁 global interpreter lock 
GIL 是Python解释器的锁，一次只能执行一个线程，其他线程必须等待，所以多线程并不能充分利用CPU的性能优势(线程安全)

内存资源 一个进程 有多个线程共享(线程不安全)
例如： 文件操作，数据库操作(事务) 
a = 3
线程A: a+=1
线程B: b+=1
结论：线程不安全，原因是CPU速度大于磁盘IO速度，线程被阻塞等待
解决： 1. 采用队列 2. 使用锁 3. 多进程 

多进程 进程通信技术

cpu密集型： 编译器优化，多线程无法达到预期效果，使用多进程
IO密集型的程序：查询数据库，文件读写，请求网络资源
结论：python适合io密集型，不适合cpu密集型
'''


''' 开启flask多线程所带来的问题
app.run(host='0.0.0.0',debug=a.config['DEBUG'],port=82) 默认是单进程，单线程，请求需要一个一个的处理，会阻塞（需要排队）
如何开启多线程?
threaded=True 
app.run(host='0.0.0.0',debug=a.config['DEBUG'],port=82,threaded=True) 开启多进程后，仍然会阻塞，因为windows不支持多进程
'''

''' 线程隔离
python中如何进行线程隔离？
使用字典来实现线程隔离，每个线程都有自己的字典(使用线程id进行区分)
'''