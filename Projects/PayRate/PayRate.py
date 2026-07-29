nam = input ("Enter your name: ")
print ("Hello", nam)
print (nam , "you will now enter your pay rate and hours worked.")
payrate = float(input (" enter your pay rate, this is confidential of course"))
hours = float(input (" enter your hours worked, this is confidential of course"))
TotalPay = (payrate * hours) * .8
print ("your total pay for this past cycle is", TotalPay)