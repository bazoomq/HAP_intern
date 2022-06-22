from multiprocessing import Pool
import time

start = time.time()
def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
    end = time.time()

    print(end - start)

    s = time.time()
    print(list(map(f, [1, 2, 3])))
    e = time.time()
    print(e-s)
