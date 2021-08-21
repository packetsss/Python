import requests
import cProfile
import asyncio
import pathlib
import pstats
import httpx
import time
import math
import re
import os

# Profiling means time every function call and rank by time

def slower_function(x):
    def fibonacci(x):
        if x < 2:
            return x
        return fibonacci(x - 1) + fibonacci(x - 2)

    # some slow functions
    time.sleep(2)
    fibonacci(x)
    for i in reversed(range(1099)):
        print([pow(j, 2) / (math.log10(j + 1) + 1) > j * 5 for j in range(int(math.log(pow(i + 1, 2))))])

# getting web info using requests
def count_https_in_web_pages():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/15Websites.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    htmls = []
    for url in urls:
        htmls = htmls + [requests.get(url).text]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print('finished parsing')
    time.sleep(2.0)
    print(f'{count_https=}')
    print(f'{count_http=}')
    print(f'{count_https/count_http=}')

# getting web info using httpx asyncio (about 1.5s faster)
async def better_count_https_in_web_pages():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/15Websites.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in urls)
        reqs = await asyncio.gather(*tasks)

    htmls = [req.text for req in reqs]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print('finished parsing')
    print(f'{count_https=}')
    print(f'{count_http=}')
    print(f'{count_https/count_http=}')

def main():
    r'''
    with cProfile.Profile() as pr:
        slower_function(33)
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename="./profiling.prof")
    # call `snakeviz ./profiling.prof` to see visualization
    
    11435387 function calls (29615 primitive calls) in 4.097 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    2.005    2.005    2.005    2.005 {built-in method time.sleep}
11405773/1    1.943    0.000    1.943    1.943 c:\Users\pyjpa\Desktop\Programming\Python\Python Tutorial Others\Profiler.py:13(fibonacci)  
     1099    0.133    0.000    0.133    0.000 {built-in method builtins.print}
     1099    0.006    0.000    0.010    0.000 c:\Users\pyjpa\Desktop\Programming\Python\Python Tutorial Others\Profiler.py:22(<listcomp>)  
        1    0.004    0.004    4.097    4.097 c:\Users\pyjpa\Desktop\Programming\Python\Python Tutorial Others\Profiler.py:12(slower_function)
    13706    0.003    0.000    0.003    0.000 {built-in method builtins.pow}
    12607    0.001    0.000    0.001    0.000 {built-in method math.log10}
     1099    0.001    0.000    0.001    0.000 {built-in method math.log}
        1    0.000    0.000    0.000    0.000 C:\ProgramData\Miniconda3\lib\cProfile.py:133(__exit__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

    '''
    with cProfile.Profile() as pr:
        asyncio.run(better_count_https_in_web_pages())

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(f'{pathlib.Path(__file__).parent.absolute()}/another_profiling.prof')

if __name__ == '__main__':
    main()