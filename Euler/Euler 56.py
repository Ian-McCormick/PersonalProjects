big = 0
for a in range(1,101):
    for b in range(1,101):
        word = str(a**b)
        ttl = 0
        for i in range(len(word)):
            ttl += int(word[i])
        if(big < ttl):
            big = ttl

print(big)
