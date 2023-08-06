def add(a,b):
    result = a+b
    print(result)

def subtract(a,b):
    result = a-b
    print(result)

def divide(a,b):
    result = a/b
    print(result)

def multiply(a,b):
    result = a*b
    print(result)

def computepay(hours, rate):
  if float(hours) > 40:
    over = float(hours) - 40
    reg = 40
    pay = float(reg) * float(rate) + float(over) * float(rate) * 1.5
  else:
    pay = float(hours) * float(rate)

  print ('The PAY is: ', pay)
