def main():
    n = 100
    fact = 1
    while n > 0:
        fact *= n
        n -= 1
    string = str(fact)
    ttl = 0
    for i in range(len(string)):
        ttl += int(string[i])
    print(ttl)
    
main()
