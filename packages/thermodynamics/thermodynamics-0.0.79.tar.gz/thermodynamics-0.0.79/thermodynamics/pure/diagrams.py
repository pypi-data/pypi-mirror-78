from matplotlib.pyplot import scatter, axhline, xlabel, ylabel, legend, plot,figure,show
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import CubicSpline, interp1d
from numpy import linspace, log10, array, arange, append,zeros
from .equilibrium import solve_eos, solve_VLE
from mpl_toolkits.mplot3d import Axes3D
#import plotly
#import plotly.graph_objs as go

def pv(T,tc,pc,acentric,p_0=1,method='pr',alfa_function='alfa_peng_robinson',pvt=False):
    volumes = []
    pres = linspace(p_0,pc)
    R=83.14
    pressures=[]
    for p in pres:
        x=solve_eos(T,p,tc,pc,acentric,method=method,alfa_function=alfa_function,diagram=True)
        if(isinstance(x,tuple)):
            volumes.append(x[0]*R*T/p)
            volumes.append(x[1]*R*T/p)
            volumes.append(x[2]*R*T/p)
            pressures.append(p)
            pressures.append(p)
            pressures.append(p)
        else:
            volumes.append(x*R*T/p)
            pressures.append(p)
            
    if(pvt):
        return(array(pressures),array(volumes))

    scatter(log10(volumes),pressures)
    axhline(pc, color='k', linestyle='--')
    xlabel('log Volume [cm3]')
    ylabel('Pressure [bar]')
    legend(['Critical pressure','PV'])
    
    return 0 


def pt(tc,pc,acentric,p_0=1,t_0=298,method='pr',alfa_function='alfa_peng_robinson',pvt=False):
    R=83.14
    pressures = linspace(p_0,pc)
    t_first = solve_VLE(300,pressures[0],tc,pc,acentric,method=method,alfa_function=alfa_function,solving_for='temperature')
    temperatures=[t_first,]
    for i in range(1,len(pressures)):
        t = solve_VLE(temperatures[i-1],pressures[i],tc,pc,acentric,method=method,alfa_function=alfa_function,solving_for='temperature')
        temperatures.append(t)
    temperatures = array(temperatures)
    
    if(pvt):
        return (pressures,temperatures)
    
    plot(temperatures,pressures)
    axhline(pc, color='k', linestyle='--')
    xlabel('Temperature (K)')
    ylabel('Pressure [bar]')
    legend(['L-V','Critical pressure'])
    

def tv(P,tc,pc,acentric,t_0=298,method='pr',alfa_function='alfa_peng_robinson',pvt=False,temperatures_array=None, atomo4=False):
    volumes = []
    if(pvt):
        temp = temperatures_array
    else:
        temp = linspace(t_0,tc)
        
    R=83.14
    temperatures=[]
    for t in temp:
        x=solve_eos(t,P,tc,pc,acentric,method=method,alfa_function=alfa_function,diagram=True)
        if(isinstance(x,tuple)):
            volumes.append(x[0]*R*t/P)
            volumes.append(x[1]*R*t/P)
            volumes.append(x[2]*R*t/P)
            temperatures.append(t)
            temperatures.append(t)
            temperatures.append(t)
        else:
            volumes.append(x*R*t/P)
            temperatures.append(t)

    if(pvt or atomo4):
        return (temperatures,volumes)
    
    scatter(log10(volumes),temperatures)
    axhline(tc, color='k', linestyle='--')
    xlabel('log Volume [cm3]')
    ylabel('Temperature [K]')
    legend(['Critical temperature','TV'])
    
    return 0 

def pvt(tc,pc,acentric,t_0=298,p_0=1,method='pr',alfa_function='alfa_peng_robinson', atomo4=False):
    temp = linspace(t_0,tc)
    general_pressures=array([])
    general_volumes=array([])
    general_temperatures=array([])
    i=1
    for T in temp:
        pressures,volumes = pv(T,tc,pc,acentric,p_0=1,method=method,alfa_function=alfa_function,pvt=True)
        aux=zeros(pressures.shape)
        aux.fill(T)
        general_volumes=append(general_volumes,volumes)
        general_pressures=append(general_pressures,pressures)
        general_temperatures=append(general_temperatures,aux)
        
    general_volumes=log10(general_volumes)

    if (atomo4):
        return (general_volumes, general_temperatures, general_pressures)
    
    #plotly.offline.init_notebook_mode()
    #fig = go.Figure(data=[go.Surface(z=general_pressures, x=general_volumes, y=general_temperatures)])
    #fig.update_layout(title='PVT',margin=dict(l=0, r=0, b=0, t=0))
    #plotly.offline.iplot(fig)
    
    fig = figure(figsize=[8,8])
    ax = fig.gca(projection='3d')

    ax.plot_trisurf(general_volumes, general_temperatures, general_pressures, linewidth=0.2, antialiased=True)
    ax.set_xlabel('log Volume [cm3]')
    ax.set_ylabel('Temperature [K]')
    ax.set_zlabel('Pressure [bar]')

    
    
    