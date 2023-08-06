from .equilibrium import bubble_temperature,bubble_pressure, dew_temperature, dew_pressure
from numpy import max, array,arange, absolute, linspace
from matplotlib.pyplot import scatter, axhline, xlabel, ylabel, legend, plot,figure,show



def pt(tc,pc,acentric,liq_compositions,vap_compositions,kij,method='pr',alfa_function='alfa_peng_robinson',mixing_rule='van_der_waals',points=100):
    tc = array(tc)
    pc=array(pc)
    max_pressure = max(pc)
    acentric=array(acentric)
    liq_compositions=array(liq_compositions)
    vap_compositions=array(vap_compositions)
    kij= array(kij)
    pressures = linspace(1,max_pressure,points)
    
    aux1=bubble_temperature(298,pressures[0],tc,pc,acentric,liq_compositions,vap_compositions,kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    aux2=dew_temperature(298,pressures[0],tc,pc,acentric,liq_compositions,vap_compositions,kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
    bubble_temperatures=[aux1[0],]
    dew_temperatures=[aux2[0],]
    for i in range(1,len(pressures)):
        aux1 = bubble_temperature(aux1[0],pressures[i],tc,pc,acentric,liq_compositions,aux1[3],kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        aux2 = dew_temperature(aux2[0],pressures[i],tc,pc,acentric,aux2[2],vap_compositions,kij,method=method,alfa_function=alfa_function,mixing_rule=mixing_rule)
        
        if(absolute(aux1[0]-aux2[0]) <= 1 or absolute(aux1[0]-bubble_temperatures[-1])<=0.1  or absolute(aux2[0]-dew_temperatures[-1])<=0.1):
            break
        bubble_temperatures.append(aux1[0])
        dew_temperatures.append(aux2[0])

    #figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    plot(bubble_temperatures,pressures[:len(bubble_temperatures)],'b',label='Bubble line')
    plot(dew_temperatures,pressures[:len(dew_temperatures)],'r',label='Dew line')
    xlabel('Temperature [K]')
    ylabel('Pressure [bar]')
    legend()
