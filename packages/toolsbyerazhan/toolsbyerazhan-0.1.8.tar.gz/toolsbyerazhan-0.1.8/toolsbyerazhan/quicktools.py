def whether_to_transfer(x:float,y:float):
    
    v1 = int(x * 37700)
    v2 = int(y * 50500)
    diff = v1 - v2

    print("value of 601699:", v1)
    print("value of 601666:", v2)
    print("the difference is:", diff)
    
    if diff > 0:
        print("Congratulations! It is time to transfer.")
    else:
        print("It is not the right time to transfer, please be patient and wait!")

