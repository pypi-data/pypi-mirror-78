from .equilibrium import bubble_temperature,bubble_pressure, dew_temperature, dew_pressure
from numpy import max, array,arange, absolute, linspace
from matplotlib.pyplot import scatter, axhline, xlabel, ylabel, legend, plot,figure,show

def pressure_composition(t,tc,pc,acentric,kij,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals',points=100):
    tc = array(tc)
    pc=array(pc)
    acentric=array(acentric)
    kij= array(kij)
    a =linspace(0,1,points)
    b=1-a
    liq_compositions=[]
    for i in range(0,len(a)):
        liq_compositions.append([a[i],b[i]])
    liq_compositions=array(liq_compositions)
    vap_compositions=liq_compositions

    aux1=bubble_pressure(t,1,tc,pc,acentric,liq_compositions[0],vap_compositions[0],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    aux2=dew_pressure(t,1,tc,pc,acentric,liq_compositions[0],vap_compositions[0],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    bubble_pressures=[aux1[1],]
    dew_pressures=[aux2[1],]
    
    for i in range(1,len(liq_compositions)):
        aux1=bubble_pressure(t,bubble_pressures[-1],tc,pc,acentric,liq_compositions[i],vap_compositions[i],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        aux2=dew_pressure(t,dew_pressures[-1],tc,pc,acentric,liq_compositions[i],vap_compositions[i],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        bubble_pressures.append(aux1[1])
        dew_pressures.append(aux2[1])

    figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plot(liq_compositions[:,:1],bubble_pressures,'b',label='Bubble line')
    plot(vap_compositions[:,:1],dew_pressures,'r',label='Dew line')
    xlabel('x,y')
    ylabel('Pressure [bar]')
    legend()
    

    
    

def temperature_composition(p,tc,pc,acentric,kij,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals',points=100):
    tc = array(tc)
    pc=array(pc)
    acentric=array(acentric)
    kij= array(kij)
    a =linspace(0,1,points)
    b=1-a
    liq_compositions=[]
    for i in range(0,len(a)):
        liq_compositions.append([a[i],b[i]])
    liq_compositions=array(liq_compositions)
    vap_compositions=liq_compositions

    aux1=bubble_temperature(298,p,tc,pc,acentric,liq_compositions[0],vap_compositions[0],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    aux2=dew_temperature(298,p,tc,pc,acentric,liq_compositions[0],vap_compositions[0],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    bubble_temperatures=[aux1[0],]
    dew_temperatures=[aux2[0],]
    
    for i in range(1,len(liq_compositions)):
        aux1=bubble_temperature(bubble_temperatures[-1],p,tc,pc,acentric,liq_compositions[i],vap_compositions[i],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        aux2=dew_temperature(dew_temperatures[-1],p,tc,pc,acentric,liq_compositions[i],vap_compositions[i],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        bubble_temperatures.append(aux1[0])
        dew_temperatures.append(aux2[0])
      
    figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plot(liq_compositions[:,:1],bubble_temperatures,'b',label='Bubble line')
    plot(vap_compositions[:,:1],dew_temperatures,'r',label='Dew line')
    xlabel('x,y')
    ylabel('Temperature [K]')
    legend()
