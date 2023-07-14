classdef Aircraft < handle
   properties
      acType % aircraft types
      velHmin % minimal horizontal velocity
      velHmax % maximal horizontal velocity
      velVmin % minimal vertical velocity
      velVmax % maximal vertical velocity
      nomSpeed % nominal speed of the AC
      accH % maximal horizontal acceleration
      accV % maximal vertical acceleration
      refP % reference positions
      refV % reference velocities
      pf % target set center position
      vf % target velocity
      p0 % initial position
      v0 % initial velocity
      pi % intermediate position where LOS happens
      timeSec % aircraft estimated time in the sector
      movVer % A/C changes vertically (climb/descent/maintain)
      hChg % change in horizontal speed required
      vChg % change in vertical speed required
      company % company A/C belongs to
   end
   methods
      function obj = Aircraft(acType,company)
         if nargin > 0
             obj.acType = acType;
             obj.setACConstraints();
             obj.company = company;
         end
      end
      function obj = setACConstraints(obj)
         switch obj.acType
             case 1
                obj.nomSpeed = 7;
                obj.velHmin = obj.nomSpeed * 0.8;
                obj.velHmax = obj.nomSpeed * 1.1;
                obj.velVmin = -2.0; 
                obj.velVmax =  1.5;
                obj.accH = 11;
                obj.accV = 58;
            case 2
                obj.nomSpeed = 6;
                obj.velHmin = obj.nomSpeed * 0.8;
                obj.velHmax = obj.nomSpeed * 1.1;
                obj.velVmin = -2.0 * 0.8; 
                obj.velVmax =  1.5 * 0.8;
                obj.accH = 11 * 0.8;
                obj.accV = 58 * 0.8;
         end
      end
      function obj = setInitFinal(obj,p0,pf,pi,v0,vf)
        obj.p0 = p0;
        obj.pf = pf;
        obj.pi = pi;
        obj.v0 = v0;
        obj.vf = vf;
        if pf(3) > p0(3) 
            obj.movVer = 1;
        elseif pf(3) < p0(3)
            obj.movVer = -1;
        else
            obj.movVer = 0;
        end
        if norm(vf(1:2),2) > norm(v0(1:2),2)
            obj.hChg = 1;
        elseif norm(vf(1:2),2) < norm(v0(1:2),2)
            obj.hChg = -1;
        else
            obj.hChg = 0;
        end
        if vf(3) > v0(3) 
            obj.vChg = 1;
        elseif vf(3) < v0(3)
            obj.vChg = -1;
        else
            obj.vChg = 0;
        end
      end
      function obj = setRefTraj(obj,refP,refV,timeSec)
        obj.refP = refP;
        obj.refV = refV;
        obj.timeSec = timeSec;
      end
      function vnom = getVnom(obj)
          vnom = obj.nomSpeed;
      end
      function pi = getPi(obj)
          pi = obj.pi;
      end
      function p0 = getP0(obj)
          p0 = obj.p0;
      end
      function pf = getPf(obj)
          pf = obj.pf;
      end
      function refP = getRefP(obj)
          refP = obj.refP;
      end
      function timeSec = getTimeSec(obj)
          timeSec = obj.timeSec;
      end
      function acType = getAcType(obj)
          acType = obj.acType;
      end
      function company = getCompany(obj)
          company = obj.company;
      end
   end
end