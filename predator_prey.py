import numpy as np
from scipy.integrate import odeint
#from array import array
import matplotlib.pyplot as plt

a = 1
b = 0.1
c = 1.5
d = 0.075

# function that returns dy/dt
def model(y,t):
    dy0dt = a * y[0] - b * y[0] * y[1]
    dy1dt = -c * y[1] + d * y[0] * y[1]
    return [dy0dt,dy1dt]

# initial condition
y0 = [2, 10]                     # initials conditions: 10 rabbits and 5 foxes  

# time points
length = 50
t = np.linspace(0,length,length*1000)
L = len(t)

# solve ODEs
y, infodict = odeint(model,y0,t, full_output=True)
infodict['message']                     # >>> 'Integration successful.'

# Plot the time course of the solution

plt.plot(t, y[:,0], 'r-', label='Rabbits')
plt.plot(t, y[:,1]  , 'b-', label='Foxes')
plt.grid()
plt.legend(loc='best')
plt.xlabel('time')
plt.ylabel('population')
plt.title('Evolution of fox and rabbit populations')
plt.show()

#------------------------------------------------------------

# We will plot some trajectories in a phase plane for different starting
# points 

#fixed points
y_f0 = np.array([ 0. ,  0.])
y_f1 = np.array([ c/d, a/b])

values  = np.linspace(0.3, 0.9, 5)    # position of y0 between y_f0 and y_f1

for v in values:
    y0 = v * y_f1                     # starting point
    y = odeint( model, y0, t)         # we don't need infodict here
    plt.plot( y[:,0], y[:,1], lw=3.5*v, label='y0=(%.f, %.f)' % ( y0[0], y0[1]) )


plt.title('Trajectories')
plt.xlabel('Number of rabbits')
plt.ylabel('Number of foxes')
plt.legend(loc='best')
plt.grid()
#plt.show()

#-------------------------------------------------------------------
# define a grid and compute direction at each point
xx = np.linspace(0, 60, 30)
yy = np.linspace(0, 40, 20)
X1 , Y1  = np.meshgrid(xx, yy)                  # create a grid
DX1, DY1 = model([X1, Y1],t=0)                  # compute growth rate on the gridt
M = (np.hypot(DX1, DY1))                        # Norm of the growth rate 
M[ M == 0] = 1.                                 # Avoid zero division errors 
#DX1 /= M                                        # Normalize each arrows
#DY1 /= M 

#the nullclines are y=a/b and x=c/d 

plt.title('Nullclines and direction fields')
Q = plt.quiver(X1, Y1, DX1, DY1)
plt.plot([c/d,c/d],[0,40],'b--',label='nullcline 1')
plt.plot([0,60],[a/b,a/b],'r--',label='nullcline 2')
plt.xlabel('Number of rabbits')
plt.ylabel('Number of foxes')
plt.grid()
plt.show()



