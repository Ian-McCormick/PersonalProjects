def factors(num):
    ttl = 0
    for i in range(1, num//2 +1):
        if(num % i == 0):
            ttl += i
    return ttl

def isAmicable(num):
    b = factors(num)
    a = factors(b)
    if((a == num) and (b != num)):
        return num
    return 0

def main():
    ttl = 0
    for i in range(0, 10000):
        ttl += isAmicable(i)
    print(ttl)
main()
