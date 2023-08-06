from scipy.misc import derivative
from numpy import exp,log

def a_fun(t,tc,pc,acentric,omega_a,alfa):
    R = 83.14
    return omega_a*(R*tc)**2*alfa/pc

def b_fun(tc,pc,omega_b):
    R = 83.14
    return omega_b*(R*tc)/pc

def A_fun(t,p,tc,pc,acentric,omega_a,alfa):
    R = 83.14
    a = a_fun(t,tc,pc,acentric,omega_a,alfa)
    A = (a*p)/(R*t)**2
    return A

def dAdT_fun(t,p,tc,pc,acentric,omega_a,alfa):
    R=83.14
    dalfa=derivative(alfa,t,args=(tc,acentric))
    
    d_a = a_fun(t,tc,pc,acentric,omega_a,dalfa)
    return(t*d_a)*(p/(R*t)**2)

def B_fun(t,p,tc,pc,omega_b):
    R = 83.14
    b=b_fun(tc,pc,omega_b)
    B=(b*p)/(R*t)
    return B

def alfa_coefficient(B,u):
    return 1-(u-1)*B

def beta_coefficient(A,B,u,w):
    return A -u*B -u*B**2 +w*B**2

def gamma_coefficient(A,B,u,w):
    return A*B+w*B**2+w*B**3

def getCubicCoefficients(A,B,u,w):
    alfa = alfa_coefficient(B,u)
    beta = beta_coefficient(A,B,u,w)
    gamma = gamma_coefficient(A,B,u,w)
    return(alfa,beta,gamma)

def getPureFugacity(z,A,B,L,p):
    ln_fugacity_coef = -log(z-B) + (z-1) - A/B *L(z,B)
    fugacity = exp(ln_fugacity_coef)*p
    return fugacity

def getMixFugacity(z,A,B,A_i,Bi,L,compositions,p):
    ln_fugacity_coef = -log(z-B)+(z-1)*(Bi/B)+(A/B)*((Bi/B)-(A_i/A))*L(z,B)
    fugacity = exp(ln_fugacity_coef)*compositions*p
    return fugacity

def getMixFugacityCoef(z,A,B,A_i,Bi,L):
    ln_fugacity_coef = -log(z-B)+(z-1)*(Bi/B)+(A/B)*((Bi/B)-(A_i/A))*L(z,B)
    fugacity_coef = exp(ln_fugacity_coef)
    return fugacity_coef
    