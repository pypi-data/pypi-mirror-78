from numpy import sqrt, log

def selector(method):
    if(method=='pr'):
        cubic = peng_robinson
    elif(method=='rks'):
        cubic = redlich_kwong_soave
    else:
        return 'Method: ' + method + ' does not exist, define an allowed method'
    return cubic
    
def peng_robinson():
    u=2
    w=-1
    omega_a = 0.45723553
    omega_b = 0.077796074
    
    def L(z,B):
        return log((z+B*(1+sqrt(2)))/(z+B*(1-sqrt(2))))/(2*sqrt(2))
    
    return (u,w,omega_a,omega_b,L)


def redlich_kwong_soave():
    u=1
    w=0
    omega_a = 0.42748023
    omega_b = 0.08664035
    
    def L(z,B):
        return (log((z+B)/z))
    
    return (u,w,omega_a,omega_b,L)
