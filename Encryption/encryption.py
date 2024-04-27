def

def new_listing(password):
    name = input("Enter Name: ")
    comp = input("Composition: ")
    return

def print_entry(password):
    return

def try_int(input):
    try:
        num = int(input)
    except ValueError:
        num = -1
    return num

def main():
    pw = input("Enter Password: ")
    while True:
        raw = input("What do you want to do?\n1)New Entry\n2)Read Entry\n3)change password\n4)exit\nyour choice: ")
        choice = try_int(raw)
        if(choice == 1):
            new_listing()
        if(choice == 2):
            print_entry()
        if(choice == 3):
            pw = input("Enter Password: ")
        if (choice == 4):
            break