from basiccompare import ValComparator

if __name__ == '__main__':
    try:
        x1 = input("Enter Num 1: ")
        x2 = input("Enter Num 2: ")
        
        o = ValComparator(x1, x2)
        print(x1, "is greater than", x2, ":", o.greater())
        print(x1, "is equal than", x2, ":", o.equal())
        print(x1, "is less than", x2, ":", o.less())
    except:
        print("Input Error")