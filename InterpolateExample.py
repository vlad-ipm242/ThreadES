"""Інтерполяція швидкості різання за табличними даними"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import *
from ThreadingV import *

V=V1pd()
D=(V['Dmax']+V['Dmin'])/2
v=V['Сталь конструкційна'].values
Vmin=np.array(v.tolist())[:,1] # Увага! Друге значення максимальне
Vmax=np.array(v.tolist())[:,0]
Vavr=(Vmin+Vmax)/2
vavr = interp1d(D, Vavr, kind='quadratic') # інтерполяція квадратичним сплайном
vmin = interp1d(D, Vmin, kind='quadratic')
vmax = interp1d(D, Vmax, kind='quadratic')
Pmin=V['Pmin'].values
Pmax=V['Pmax'].values
pmin = interp1d(D, Pmin, kind='linear')
pmax = interp1d(D, Pmax, kind='linear')

# аналог map в Arduino
# або interp1d([x1, x2], [y1, y2], kind='linear')
def map_value(x, x1, x2, y1, y2):
    k=(x-x1)/(x2-x1)
    y=y1+k*(y2-y1)
    return y

def Vinterp(D, P):
    "Інтерполяція швидкості за D, P"
    pmn, pmx = pmin(D), pmax(D)
    if P<pmn: return vmax(D)
    if P>pmx: return vmin(D)
    vmn, vmx = vmin(D), vmax(D)
    V=map_value(P, pmn, pmx, vmx, vmn) # vmn, vmx поміняно місцями. Більше значення V приймають для різьб з меньшим P
    return V

print(Vinterp(10, 1.5))

X=np.arange(5,45,0.1)
plt.plot(X, pmin(X)*10, 'k--'); plt.plot(D, Pmin*10, 'k^')
plt.plot(X, pmax(X)*10, 'k--'); plt.plot(D, Pmax*10, 'k^')
plt.plot(X, vavr(X), 'k'); plt.plot(D, Vavr, 'ko')
plt.plot(X, vmin(X), 'r'); plt.plot(D, Vmin, 'ro')
plt.plot(X, vmax(X), 'r'); plt.plot(D, Vmax, 'ro')
plt.plot(X, [Vinterp(x, 1.0) for x in X], 'k:'); plt.plot(D, [Vinterp(x, 1.0) for x in D], 'k*')
plt.xlabel('$D$, мм'); plt.ylabel('$V$, м/хв; $P$, мм/10');
plt.grid()
plt.show()

##
D=np.array([(j,i) for i,j in V['D']])
D=D.reshape(D.size)
P=np.array([(i,j) for i,j in V['P']])
P=P.reshape(P.size)
v=np.array([(i,j) for i,j in V['Сталь конструкційна']])
v=v.reshape(v.size)

f = CloughTocher2DInterpolator(list(zip(D,P)), v, rescale=True)
print(f(6, 0.5), f(3, 1), f(6, 1), f(3, 0.5))
f2 = NearestNDInterpolator(list(zip(D,P)), v, rescale=True)
print(f2(6, 0.5), f2(3, 1), f2(6, 1), f2(3, 0.5))
ap=[(0,0),(50,0),(50,3),(0,3)]
fap=[f2(x,y) for x,y in ap]
f3 = CloughTocher2DInterpolator(list(zip(D,P))+ap, v.tolist()+fap, rescale=True)

def COMBinterp(x, y, f, f2):
    res = f(x, y)
    mask = np.isnan(res)
    res2= f2(x, y)
    res[mask] =res2[mask]
    return res

print(COMBinterp(10, 1.5, f, f2))

X, Y = np.meshgrid(np.arange(0., 50.1, 0.1), np.arange(0., 3.1, 0.1))
Z = f3(X,Y)
#Z = COMBinterp(X, Y, f, f2)
plt.plot(D, P, "or")
plt.pcolormesh(X, Y, Z)
plt.colorbar()
plt.xlabel('$D$, мм'); plt.ylabel('$P$, мм');
plt.show()

