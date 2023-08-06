from numpy import array,sum, sqrt
from scipy.misc import derivative

def selector(mixing_rule):
    if(mixing_rule == 'van_der_waals'):
        return van_der_waals
    else:
        return 'Mixing rule does not exist'

def van_der_waals(compositions,tc,acentric,kij,Ai,Bi,alfa,alfa_fun,T):
    shape = kij.shape
    B = sum(compositions*Bi)
    Aij=array([sqrt(Ai[i]*Ai[j])*(1-kij[i,j]) for i in range(0,len(Ai)) for j in range(0,len(Ai))]).reshape(shape)
    A = sum([sum(compositions[i]*compositions[j]*Aij[i,j]) for i in range(0,len(Ai)) for j in range(0,len(Ai))])
    A_i = array([(compositions[j]*Aij[:,j]) for j in range(0,len(Ai))])
    A_i =array([2* sum(A_i[:,i]) for i in range(0,len(Ai))])
    dAdT = sum([0.5*sum(compositions[i]*compositions[j]*Aij[i,j]*((T/alfa[i])*derivative(alfa_fun,T,args=(tc[i],acentric[i]))+(T/alfa[j])*derivative(alfa_fun,T,args=(tc[j],acentric[j])))) for i in range(0,len(Ai)) for j in range(0,len(Ai))])
    return (A,B,A_i,Aij,dAdT)
