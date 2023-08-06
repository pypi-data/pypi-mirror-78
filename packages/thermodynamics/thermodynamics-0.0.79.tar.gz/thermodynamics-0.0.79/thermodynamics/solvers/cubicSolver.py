from numpy import sqrt, arccos, absolute, cos, pi

def cubic_solver_not_used(coefficients,diagram,B):
    alfa,beta,gamma = coefficients
    alfa= -1*alfa
    p=(3*beta-alfa**2)/3
    q=(27*gamma-9*alfa*beta+2*alfa**3)/27
    R=(p/3)**3+(q/2)**2

    if(R>0):
        first = -q*0.5+sqrt(R)
        second = -q*0.5-sqrt(R)
        
        if(second >0 and first >0 ):
            x = first**(1/3)+second**(1/3)-alfa/3
        elif(second>0 and first<0):
            x = -(-1*first)**(1/3) + second**(1/3)-alfa/3
        elif(second<0 and first>0):
            x = first**(1/3) -(-1*second)**(1/3)-alfa/3
        else:
            x = -(-1*first)**(1/3)-(-1*second)**(1/3)-alfa/3
        return x
        
    elif(R<0):
        theta = arccos(((-27/4)*(q**2/p**3))**(0.5))
        x1=-2*(absolute(q)/q)*(-p/3)**0.5 * cos(theta/3)-alfa/3
        x2=-2*(absolute(q)/q)*(-p/3)**0.5 * cos(theta/3+(2*pi/3))-alfa/3
        x3=-2*(absolute(q)/q)*(-p/3)**0.5 * cos(theta/3+(4*pi/3))-alfa/3
        x = [x1,x2,x3]
        return (min(x),max(x))
    else:
        raise Exception("cubic solver error")
    

def cubic_solver(coefficients,diagram,B):
    alfa,beta,gamma = coefficients
    C = 3*beta - alfa**2
    D = -alfa**3 + 4.5*alfa*beta-13.5*gamma
    Q = C **3 + D **2

    if(Q<= 0):
        theta = arccos(-D/(sqrt(-C**3)))
        
        z_liq = (alfa + 2* sqrt(-C)*cos(theta/3+(2*pi/3)))/3
        z_vap = (alfa + 2* sqrt(-C)*cos(theta/3))/3
        
        
        if (diagram):
            z_extra =  (alfa + 2* sqrt(-C)*cos(theta/3+(4*pi/3)))/3
            return(z_vap,z_liq,z_extra)
        
        if(z_liq < B):
            z_liq = (alfa + 2* sqrt(-C)*cos(theta/3))/3
        
        return (z_liq,z_vap)
        
    elif(Q>0):
        first = -D+sqrt(Q)
        second = -D-sqrt(Q)
        aux1=False
        aux2=False
        if(first<0):
            first *= -1
            aux1 = True
        if(second<0):
            second *= -1
            aux2 = True
            
            
        z = (alfa+(-1 if(aux1)else 1)*(first)**(1/3)+(-1 if(aux2) else 1)*(second)**(1/3))/3
        
        return z
    
    else:
        raise Exception("cubic solver error")
    
        