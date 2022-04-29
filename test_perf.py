import requests
import time,timeit
import  threading
hostName = "localhost"
serverPort = 8080
url = "http://localhost:8080/try_it"
post_data = {"try" : "1","try2" : "2",
             "try3" : "1","try4" : "2"}


def send():
    x = requests.post(url,json=post_data)
    if x.status_code == 200:
        return
    else:
        print('error',x.status_code)

def main():
    threads = []
    for i in range(100):
        t = threading.Thread(target=send,args=())
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
if __name__ == "__main__":
    t = timeit.Timer(main)
    print(t.timeit(number=5))
