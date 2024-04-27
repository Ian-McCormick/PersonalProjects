def split(num):
    digits = ["0", "0", "0", "0"]
    for i in range(1, 5):
        digits[4-i] = str(num % 10)
        num = num // 10
    return digits

def count(num):
    digits = split(num)
    ttl = 0
    if(digits[2] == '1'):   #check if there is a "teen" in the number
        ttl += teens[digits[3]]
    else:                   #if not, use standard ones and tens
        if(digits[3] != '0'):   #convert the ones place
            ttl += ones[digits[3]]
        if(digits[2] != '0'):   #convert the tens place
            ttl += tens[digits[2]]
            
    if(num > 99):      
        if(num%100 != 0):       #if num isn't a multiple of 100, we need to include the 'and'
            ttl += 3
        if(digits[1] != '0'):   #convert the hundreds place
            ttl += ones[digits[1]] + 7
        if(digits[0] != '0'):   #convert the thousands place
            ttl += ones[digits[0]] + 8
    return ttl
    
def main():
    global ones
    global teens
    global tens
    
    ones = {"1" : 3, "2" : 3, "3" : 5, "4" : 4, "5" : 4, "6" : 3, "7" : 5, "8" : 5, "9" : 4}
    teens = {"0": 3, "1" : 6, "2" : 6, "3" : 8,"4" : 8, "5" : 7, "6" : 7, "7" : 9, "8" : 8, "9" : 8}
    tens = {"2" : 6, "3" : 6, "4" : 5, "5" : 5, "6" : 5, "7" : 7, "8" : 6, "9" : 6}

    total = 0
    for i in range(1, 1001):
        total += count(i)
    print(total)
    
main()
