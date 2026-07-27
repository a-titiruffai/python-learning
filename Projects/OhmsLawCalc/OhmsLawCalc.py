print ("Hello, This is an Ohms Law Calculator")
print ("This is just a basic project beacuse I wanted to make a commit but was out today as its my 18th bday,07/25/26!!!")
print ("Anyways to select a value to calculate insert the following: 1 for Voltage, 2 for Current, 3 for Resistance")
while True:
    select = input("Which Value?")
    if select == "1":
            print ("You have selected Voltage")
            I = float(input("Current?"))
            R = float(input ("Resistance?"))
            V = float(I) * float(R)
            print (V,"Volts")
            break
    elif select == "2":
            print ("You have selected Current")
            V = float(input("Voltage?"))
            R = float(input ("Resistance?"))
            I = float(V) / float(R)
            print (I, "Amps")
            break
    elif select == "3":
            print ("You have selected Resistance")
            V = float(input("Voltage?"))
            I = float(input ("Current?"))
            R = float(V) / float(I)
            print (R,"ohms")
            break
    else:
            print("Invalid Choice. Try Again")