def main():
    fib = [1, 1]
    while True:
        new = fib[-1] + fib[-2]
        if(len(str(new)) >= 1000):
            fib.append(new)
            print(len(fib))
            break
        else:
            fib.append(new)
    print("Done")
main()
