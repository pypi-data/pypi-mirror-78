from numpy import exp


    
def selector(number):
    if(number == '4'):
        return eq_4
    
    elif(number == '16'):
        return eq_16

    else:
        return None

def eq_4(t,constants):
    a,b,c,d = constants
    return (a+b*t+c*t**2+d*t**3)

def eq_16(t,constants):
    a,b,c,d,e = constants
    return (a+exp(b/t)+c+d*t+e*t**2)
