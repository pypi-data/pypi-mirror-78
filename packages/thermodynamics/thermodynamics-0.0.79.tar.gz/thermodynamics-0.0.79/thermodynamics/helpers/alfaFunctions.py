from numpy import sqrt, exp, where

def selector(alfa_function):
    if(alfa_function == 'soave'):
        fun = soave
    elif(alfa_function == 'alfa_peng_robinson'):
        fun=alfa_peng_robinson
    elif(alfa_function == 'pr78'):
        fun = pr78
    elif(alfa_function == 'mathias'):
        fun = mathias
    elif(alfa_function == 'stryjek_vera'):
        fun = stryjek_vera
    else:
        return 'Function: ' + alfa_function+ 'does not exist provide a valid function'
    return fun
    
def soave(t,tc,acentric):
    m = 0.48508 + 1.55171*acentric-0.15613*acentric**2
    reduced_temperature=t/tc
    return (1+m*(1-sqrt(reduced_temperature)))**2

def alfa_peng_robinson(t,tc,acentric):
    m=0.37464+1.54226*acentric-0.26992*acentric**2
    reduced_temperature=t/tc
    return (1+m*(1-sqrt(reduced_temperature)))**2

def pr78(t,tc,acentric):
    #if(acentric>0.49):
    #    m=0.379642+1.48503*acentric-0.164423*acentric**2+0.016666*acentric**3
    #else:
    #    m=0.37464+1.54226*acentric-0.26992*acentric**2
    m = where(acentric>0.49,0.379642+1.48503*acentric-0.164423*acentric**2+0.016666*acentric**3,0.37464+1.54226*acentric-0.26992*acentric**2)
    reduced_temperature=t/tc
    return (1+m*(1-sqrt(reduced_temperature)))**2


def mathias(t,tc,acentric,qi=0):
    reduced_temperature=t/tc
    m = 0.48508+1.55191*acentric-0.15613*acentric**2
    c = 1 + m/2 + 0.3*qi
    alfa = where(t>tc,exp(2*((c-1)/c)*(1-reduced_temperature**c)),(1+m*(1-reduced_temperature**(0.5))-qi*(1-reduced_temperature)*(0.7-reduced_temperature))**2)
        
    return alfa



def stryjek_vera(t,tc,acentric,k1):
    reduced_temperature=t/tc
    k0 = 0.378893+1.4897153*acentric-0.17131848*acentric**2+0.0196554*acentic**3
    
    if(t>tc):
        alfa = (1+k0*(1-sqrt(reduced_temperature)))**2
    else:
        alfa = (1+k0*(1-reduced_temperature**(0.5))+k1*(1-reduced_temperature)*(0.7-reduced_temperature))**2
        
    return alfa
