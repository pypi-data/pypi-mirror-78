from ..helpers import eos
from ..helpers import alfaFunctions
from ..helpers.eosHelpers import A_fun, B_fun, getCubicCoefficients, dAdT_fun, getPureFugacity
from ..solvers.cubicSolver import cubic_solver
from ..helpers import temperatureCorrelations as tempCorr
from numpy import log, exp, sqrt,absolute
from scipy.optimize import root
from scipy.integrate import quad
import json

def solve_eos(t,p,tc,pc,acentric,method='pr',alfa_function='alfa_peng_robinson',diagram=False,properties=False,heat_capacity=None):
    # Method selection
    eos_fun=eos.selector(method)
    u,w,omega_a,omega_b,L = eos_fun()

    # Alfa function selection    
    alfa_fun = alfaFunctions.selector(alfa_function)
    alfa= alfa_fun(t,tc,acentric)
    
    B = B_fun(t,p,tc,pc,omega_b)
    A = A_fun(t,p,tc,pc,acentric,omega_a,alfa)
    coefficients = getCubicCoefficients(A,B,u,w)
    

    x= cubic_solver(coefficients,diagram,B)
   
    if(diagram):
        return x
    
    if(isinstance(x,tuple)):
        z_liq = x[0]
        z_vap = x[1]
        
    else:
        z_liq=x
        z_vap=x
    
    liq_fugacity = getPureFugacity(z_liq,A,B,L,p)
    vap_fugacity = getPureFugacity(z_vap,A,B,L,p)
        
    if(properties):
        ideal_enthalpy = get_ideal_enthalpy(heat_capacity,t)/1000 # kmol to mol
        ideal_entropy = get_ideal_entropy(heat_capacity,t,p)/1000 #kmol to mol
        dAdt =  dAdT_fun(t,p,tc,pc,acentric,omega_a,alfa_fun)        
        enthalpy_liq = get_real_enthalpy(ideal_enthalpy,t,z_liq,A,dAdt,B,L)
        enthalpy_vap = get_real_enthalpy(ideal_enthalpy,t,z_vap,A,dAdt,B,L)
        entropy_liq = get_real_entropy(ideal_entropy,z_liq,A,dAdt,B,L)
        entropy_vap = get_real_entropy(ideal_entropy,z_vap,A,dAdt,B,L)

        response = {
            "liq_fugacity":liq_fugacity,
            "vap_fugacity":vap_fugacity,
            "enthalpy_liq":enthalpy_liq,
            "enthalpy_vap":enthalpy_vap,
            "entropy_liq":entropy_liq,
            "entropy_vap":entropy_vap,
            "z_liq":z_liq,
            "z_vap":z_vap
        }

        return response
    
         
    return (liq_fugacity, vap_fugacity)



def solve_VLE(t,p,tc,pc,acentric,solving_for='pressure',method='pr',alfa='alfa_peng_robinson'):
    if(solving_for=='pressure'):
        
        P = root(vle_pressure_objective_function,p,args=(t,tc,pc,acentric,method,alfa))
       
        return P.x[0]
    elif(solving_for=='temperature'):
        T = root(vle_temperature_objective_function,t,args=(p,tc,pc,acentric,method,alfa))
        
        return T.x[0]
        
def vle_pressure_objective_function(p,t,tc,pc,acentric,method='pr',alfa='alfa_peng_robinson'):
    
    liq_fugacity, vap_fugacity = solve_eos(t,p,tc,pc,acentric,method,diagram=False)
    
    return liq_fugacity-vap_fugacity

def vle_temperature_objective_function(t,p,tc,pc,acentric,method='pr',alfa='alfa_peng_robinson'):
    liq_fugacity, vap_fugacity = solve_eos(t,p,tc,pc,acentric,method,diagram=False)
    return liq_fugacity-vap_fugacity


def get_ideal_enthalpy(heat_capacity,t):
    number,constants = heat_capacity
    heat_capacity_equation =tempCorr.selector(number)
    enthalpy,_ = quad(heat_capacity_equation,298,t,args=(constants,))
    return enthalpy
    
    

def get_ideal_entropy(heat_capacity,t,p):
    R=8.314
    number,constants = heat_capacity
    heat_capacity_equation = lambda t,constants :tempCorr.selector(number)(t,constants)/t
    I,_ = quad(heat_capacity_equation,298,t,args=(constants,))
    entropy = I - R*log(p)
    return entropy


def get_real_enthalpy(ideal_enthalpy,t,z,A,dAdt,B,L):
    R=8.314
    enthalpy = ideal_enthalpy + R*t*(z-1+((dAdt-A)/B)*L(z,B))
    return enthalpy

def get_real_entropy(ideal_entropy,z,A,dAdt,B,L):
    R=8.314
    entropy = ideal_entropy + R*(log(z-B)+dAdt/B*L(z,B))
    return entropy


