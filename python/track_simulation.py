import numpy as np
from numpy import linalg
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plotCylinderWithCaps(r,cnt,height,nSides,color,alpha)
    [X,Y,Z] = cylinder(r,nSides)
    X = X + cnt[0]
    Y = Y + cnt[1]
    Z = Z * height + cnt[2]
    h1 = surf(X,Y,Z,'facecolor',color,'LineStyle','none','facealpha',alpha);
    h2 = fill3(X(1,:),Y(1,:),Z(1,:),color,'facealpha',alpha);
    h3 = fill3(X(2,:),Y(2,:),Z(2,:),color,'facealpha',alpha);
    return [h1, h2, h3]  %only needed if this is within a script

'''
Solve LOS maneuvers as an ATCO
Prof. Rubens J M Afonso
'''
def atco_label(scenario):
    maneuver = []
    # separate horizontally if wind is too strong
    # rationale: climb/descent uncertain
    if scenario.windStr > 40:
        maneuver = 'PATHSEP'
    elif scenario.windStr > 30:
        maneuver = 'SEPHORIZ'
    else:
        # get expected time to pf
        time1 = scenario.aircraft[0].getTimeSec()
        time2 = scenario.aircraft[1].getTimeSec()
        # the one that has more time to the target goes behind
        # rationale: more time to recover lost time and fast A/C
        if time1 > 1.2*time2 and scenario.aircraft[1].acType == 1:
            maneuver = 'BEFORE(2,1)'
        elif time2 > 1.2*time1 and scenario.aircraft[2].acType == 1:
            maneuver = 'BEFORE(1,2)'
    
        # if expected time to target < 4 time steps, than maintain path
        if time1 < 4*scenario.dt:
            maneuver = 'FIXPATH(1)'
        elif time2 < 4*scenario.dt:
            maneuver = 'FIXPATH(2)'
       
        # in case none of the above was selected
        if len(maneuver) == 0:
            # get final position of each aircraft
            pf1 = scenario.aircraft[0].getPf()
            pf2 = scenario.aircraft[1].getPf()
            # the one that finishes higher flies above
            if pf1(3) > pf2(3):
                maneuver = 'OVER(1,2)'
            else:
                maneuver = 'OVER(2,1)'
    return maneuver   

class Aircraft:
    def __init__(self, acType, company):
        self.acType = acType # aircraft types
        self.velHmin = None # minimal horizontal velocity
        self.velHmax = None # maximal horizontal velocity
        self.velVmin = None # minimal vertical velocity
        self.velVmax = None # maximal vertical velocity
        self.nomSpeed = None # nominal speed of the AC
        self.accH = None # maximal horizontal acceleration
        self.accV = None # maximal vertical acceleration
        self.refP = None # reference positions
        self.refV = None # reference velocities
        self.pf = None # target set center position
        self.vf = None # target velocity
        self.p0 = None # initial position
        self.v0 = None # initial velocity
        self.pi = None # intermediate position where LOS happens
        self.timeSec = None # aircraft estimated time in the sector
        self.movVer = None # A/C changes vertically (climb/descent/maintain)
        self.hChg = None # change in horizontal speed required
        self.vChg = None # change in vertical speed required
        self.company = company # company A/C belongs to
        self.__set_AC_Constraints()
    
    def __set_AC_Constraints(self):
        if self.acType == 1:
            self.nomSpeed = 7
            self.velHmin = self.nomSpeed * 0.8
            self.velHmax = self.nomSpeed * 1.1
            self.velVmin = -2.0 
            self.velVmax =  1.5
            self.accH = 11
            self.accV = 58
        elif self.acType == 2:
            self.nomSpeed = 6
            self.velHmin = self.nomSpeed * 0.8
            self.velHmax = self.nomSpeed * 1.1
            self.velVmin = -2.0 * 0.8 
            self.velVmax =  1.5 * 0.8
            self.accH = 11 * 0.8
            self.accV = 58 * 0.8

    def setInitFinal(self, p0, pf, pi, v0, vf):
        self.p0 = p0
        self.pf = pf
        self.pi = pi
        self.v0 = v0
        self.vf = vf
        if pf[2] > p0[2]:
            self.movVer = 1
        elif pf[2] < p0[2]:
            self.movVer = -1
        else:
            self.movVer = 0
        
        if linalg.norm(vf[0:1], ord=2) > linalg.norm(v0[0:1], ord=2):
            self.hChg = 1
        elif linalg.norm(vf[0:1], ord=2) < linalg.norm(v0[0:1], ord=2):
            self.hChg = -1
        else:
            self.hChg = 0
        
        if vf[2] > v0[2]:
            self.vChg = 1
        elif vf[2] < v0[2]:
            self.vChg = -1
        else:
            self.vChg = 0
        
    def setRefTraj(self, refP, refV, timeSec):
        self.refP = refP
        self.refV = refV
        self.timeSec = timeSec
    
    def getVnom(self):
        return self.nomSpeed

    def getPi(self):
        return self.pi

    def getP0(self):
        return self.p0
    
    def getPf(self):
        return self.pf
    
    def getRefP(self):
        return self.refP
    
    def getTimeSec(self):
        return self.timeSec
    
    def getAcType(self):
        return self.acType
      
    def getCompany(self):
        return self.company

'''
Generation of LOS (loss of separation) scenarios for a pair of A/C
Prof. Rubens J M Afonso
'''
class LOSScenario:
    def __init__(self, horSep, verSep, Na, secW, secL, secH, Nt, dt):
        self.horSep = horSep # horizontal separation
        self.verSep = verSep # vertical separation
        self.Na = Na # number of aircraft 
        self.secW = secW # sector width
        self.secL = secL # sector length
        self.secH = secH # sector height
        self.dt = dt # time step
        self.Nt = Nt # max number of time steps
        self.windStr = np.random.uniform(0,1,1)*45 # wind strengh
        self.aircraft = None # each A/C in the scenario
        self.setAC()

    def setAC(self):
        for i in range(0, self.Na):
            acType = np.random.randint(0, high=2, size=1)
            company = np.random.randint(0, high=3, size=1)
            self.aircraft[i] = Aircraft(acType,company)
            if i == 1:
                # intermediate in a smaller paralelepiped at the center
                alpha = 0.3
                minX = alpha * self.secW
                maxX = (1-alpha) * self.secW
                minY = alpha * self.secL
                maxY = (1-alpha) * self.secL
                minZ = (alpha-1) * self.secH
                maxZ = (1-alpha) * self.secH
                lb = np.array([[minX, minY, minZ]]).T 
                ub = np.array([[maxX, maxY, maxZ]]).T 
                pi = lb + np.random.uniform(low=0.0, high=1.0, size=3)* (ub-lb)

                # final position at the far right, midle in y and z
                pf = np.array([[0.9*self.secW, self.secL/2, 0]]).T
                # unit vector in the direction of movement
                vUnit = (pf-pi)/linalg.norm(pf-pi,2)
                # absolute values of the initial velocities
                vnom = self.aircraft[i].getVnom()
                vxy = vnom * vUnit[0:1]
                timeI2F = linalg.norm(pf[0:1]-pi[0:1],2) / vnom
                vz = (pf[2] - pi[2]) / timeI2F
                v0 = np.array([[vxy, vz]]).T
                vf = v0
                # propagate backwards until reaching the initial position
                # at the boundary of the sector
                alpha = 0.0
                minX = alpha * self.secW
                maxX = (1-alpha) * self.secW
                minY = alpha * self.secL
                maxY = (1-alpha) * self.secL
                minZ = (alpha-1) * self.secH
                maxZ = (1-alpha) * self.secH
                timeX = max((pf[0]-minX)/vxy[0],(pf[0]-maxX)/vxy(1))
                timeY = max((pf[1]-minY)/vxy[1],(pf[1]-maxY)/vxy(2))
                timeZ = max((pf[2]-minZ)/vz,(pf[2]-maxZ)/vz)
                timeSec = min([timeX,timeY,timeZ])
                p0 = pf - v0 * timeSec
                self.aircraft[i].setInitFinal(p0,pf,pi,v0,vf)
                # set reference trajectory
                self.setRefTrajAC(i)
            else:
                # intermediate in a paralelepiped around A/C 1
                minX = -self.horSep / sqrt(2)
                maxX =  self.horSep / sqrt(2)
                minY = -self.horSep / sqrt(2)
                maxY =  self.horSep / sqrt(2)
                minZ = -self.verSep
                maxZ =  self.verSep
                lb = np.array([[minX, minY, minZ]]).T 
                ub = np.array([[maxX, maxY, maxZ]]).T 
                pi = lb + np.random.uniform(0,1,3) * (ub-lb) + self.aircraft[0].getPi()
                # final position anywhere in the sector
                alpha = 0
                minX = alpha * self.secW
                maxX = (1-alpha) * self.secW
                minY = alpha * self.secL
                maxY = (1-alpha) * self.secL
                minZ = (alpha-1) * self.secH
                maxZ = (1-alpha) * self.secH
                lb = np.array([[minX, minY, minZ]]).T 
                ub = np.array([[maxX, maxY, maxZ]]).T 
                pf = lb + np.random.uniform(0,1,3) * (ub-lb)
                # unit vector in the direction of movement
                vUnit = (pf-pi)/linalg.norm(pf-pi,2)
                # absolute values of the initial velocities
                vnom = self.aircraft[i].getVnom()
                vxy = vnom * vUnit[0:1]
                timeI2F = linalg.norm(pf[0:1]-pi[0:1],2) / vnom
                vz = (pf(3) - pi(3)) / timeI2F
                v0 = np.array([[vxy, vz]]).T
                vf = v0
                # propagate backwards until reaching the initial position
                # at the boundary of the sector
                alpha = 0.0
                minX = alpha * self.secW
                maxX = (1-alpha) * self.secW
                minY = alpha * self.secL
                maxY = (1-alpha) * self.secL
                minZ = (alpha-1) * self.secH
                maxZ = (1-alpha) * self.secH
                timeX = max((pf[0]-minX)/vxy[0],(pf[0]-maxX)/vxy[0])
                timeY = max((pf[1]-minY)/vxy[1],(pf[1]-maxY)/vxy[1])
                timeZ = max((pf[2]-minZ)/vz,(pf[2]-maxZ)/vz)
                timeSec = min([timeX,timeY,timeZ])
                p0 = pf - v0 * timeSec
                self.aircraft[i].setInitFinal(p0,pf,pi,v0,vf)
                # set reference trajectory
                self.setRefTrajAC(i)

    def setInitFinalAC(self, index, p0, pf, pi, v0, vf):
        ac = self.aircraft[index]
        ac.setInitFinal(p0,pf,pi,v0,vf)
    
    def setRefTrajAC(self, index):
        ac = self.aircraft[index]
        avgV = (ac.vf + ac.v0)/2
        pLen = linalg.norm(ac.pf - ac.p0,2)
        timeSec = pLen / linalg.norm(avgV,2)
        avgAcc = (ac.vf - ac.v0) / timeSec
        aux = np.linspace(0,1,self.Nt)
        refV = ac.v0+ aux*(ac.vf - ac.v0)
#         timeVec = ([0:1:obj.Nt])' * obj.dt;
#         refP = repmat(ac.p0,obj.Nt+1,1) + kron(timeVec ,ac.v0) + kron(timeVec.^2,avgAcc / 2);
        timeVec = np.arange(0, self.Nt+1, 1) * self.dt
        refP = np.tile(ac.p0,1,self.Nt+1) + np.kron(timeVec ,ac.v0) + np.kron(timeVec**2,avgAcc / 2)
        ac.setRefTraj(refP,refV,timeSec)
      
    def plot(self):
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        h = np.zeros((self.Na,1))
        for i in range(self.Na):
            refP = self.aircraft[i].getRefP()
            h[i] = ax1.plot3D(refP[0,:], refP[1,:], refP[2,:],'*-')
            p0 = self.aircraft[i].getP0()
            pi = self.aircraft[i].getPi()
            pf = self.aircraft[i].getPf()
            ax1.plot3D(p0[0],p0[1],p0[2],'o')
            ax1.plot3D(pi[0],pi[1],pi[2],'+k')
            ax1.plot3D(pf[0],pf[1],pf[2],'s')
            plotCylinderWithCaps(self.horSep/2,pi-np.array([[0,0,self.verSep/2]]).T,self.verSep,20,[1,0,0],0.1)
            ax1.set_xlim([0, self.secW])
            ax1.set_ylim([0, self.secL])
            ax1.set_zlim([-self.secH, self.secH])
            plt.axis('square')
            ax1.legend(['A\C '+str(i+1)])
            #axis square;
        #end
        plt.grid()
        ax1.set_xlabel('$x$ (NM)','interpreter','latex')
        ax1.set_ylabel('$y$ (NM)','interpreter','latex')
        ax1.set_zlabel('$z$ (kft)','interpreter','latex')
        
        plt.show()
    
    def getWindSpeed(self):
        return self.windStr


class Track_Simulation:
      def __init__(self, tree = None, data = None):
        #if tree != None:
        #    self.tree = tree
        #else:
        #    self.__create_tree(True, data = None)
        self.data = data