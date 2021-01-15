import matplotlib.pyplot as plt
import time
import math

targetVel=2540   # mm/s
acc=7000    # mm/s2
totTime=2.0  # tempo totale movimento in s
spaceVelConst=2000  # mm di stampa a vel const.

tick=0.005  # tick time
tAcc=targetVel/acc  # moto uniform.acc.    S=1/2*a*t2    v/a=t
tVelConst=spaceVelConst/targetVel      # moto rettilineo uniforme   S=v*t
velStep=tick*acc

print("tick="+str(tick))
print("tAcc="+str(tAcc))
print("tVelConst="+str(tVelConst))
print("velStep="+str(velStep))

#teorico
velsT=[0.0] #array of velsT
tT=[0.0] #array of tick
#reale
velsR=[0.0] #array of velsR
errsP=[0.0]
errsI=[0.0]
errsD=[0.0]
errs=[0.0]
#PID pars
kP=0.9
kI=-1.1    #-1.5
kD=-0.5    #-0.5

def createData():
    velR=0.0
    cumErr=0.0
    errLast=0.0
    time.sleep(tick)   # 10ms
    t=0.0
    vel=0.0
    while True:
        t+=tick
        if t<=tAcc: #acc
            vel+=velStep
        else:   #regime
            if t>tAcc+tVelConst:    #dec
                vel-=velStep
            if t>totTime:
                break
        if vel<0:
            vel=0
        tT.append(t)
        velsT.append(vel)
        #PID count
        #global velR, cumErr, errLast
        err=vel-velR
        #print("err="+str(err))
        cumErr+=err
        deltaErr=err-errLast
        errLast=err
        eP=kP*err
        eI=kI*cumErr
        eD=kD*deltaErr
        #print("P="+str(eP)+" I="+str(eI)+" D="+str(eD))
        velR=vel-eP-eI-eD
        #print("velR="+str(velR))
        velsR.append(velR)
        errsP.append(eP)
        errsI.append(eI)
        errsD.append(eD)
        errs.append(eP+eI+eD)

createData()

fig, ax1 = plt.subplots()

ax1.set_xlabel('time (s)')
ax1.set_ylabel('velocity [mm/s]')
ax1.plot(tT,velsT,'blue', tT,velsR,'red')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.spines["left"].set_position(("axes", -0.2))
ax2.set_ylabel('error [mm/s]', )
ax2.yaxis.set_label_position('left')
ax2.yaxis.tick_left()
ax2.yaxis.set_ticks_position('left')
ax2.plot(tT,errsP,'cyan', tT,errsI,'yellow', tT,errsD,'green', tT,errs,'black')

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.plot(tT,velsT, tT,velsR, tT,errsP, tT,errsI, tT,errsD, tT,errs)
plt.ylabel('velocity [mm/s]')
plt.xlabel('time [sec]')
plt.show()
plt.savefig('fig.png')
