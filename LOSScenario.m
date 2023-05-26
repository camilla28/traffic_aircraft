% Generation of LOS (loss of separation) scenarios for a pair of A/C
% Prof. Rubens J M Afonso

classdef LOSScenario < handle
   properties
      horSep % horizontal separation
      verSep % vertical separation
      Na % number of aircraft 
      secW % sector width
      secL % sector length
      secH % sector height
      dt % time step
      Nt % max number of time steps
      windStr % wind strengh
      aircraft % each A/C in the scenario
   end
   methods
      function obj = LOSScenario(horSep,verSep,Na,secW,secL,secH,Nt,dt)
         input = [horSep,verSep,Na,secW,secL,secH,Nt,dt];
         if nargin > 0
            obj.horSep = input(1);
            obj.verSep = input(2);
            obj.Na = input(3);
            obj.secW = input(4);
            obj.secL = input(5);
            obj.secH = input(6);
            obj.Nt = input(7);
            obj.dt = input(8);
            obj.windStr = rand(1,1)*45;
            obj.setAC();
         end
      end
      function obj = setAC(obj)
         for i = 1:obj.Na
             acType = randi(2,1);
             company = randi(3,1);
             obj.aircraft{i} = Aircraft(acType,company);
             if i == 1
                % intermediate in a smaller paralelepiped at the center
                alpha = 0.3;
                minX = alpha * obj.secW;
                maxX = (1-alpha) * obj.secW;
                minY = alpha * obj.secL;
                maxY = (1-alpha) * obj.secL;
                minZ = (alpha-1) * obj.secH;
                maxZ = (1-alpha) * obj.secH;
                lb = [minX; minY; minZ];
                ub = [maxX; maxY; maxZ];
                pi = lb + rand(3,1) .* (ub-lb);
%                 % final position anywhere in the sector
%                 alpha = 0;
%                 minX = alpha * obj.secW;
%                 maxX = (1-alpha) * obj.secW;
%                 minY = alpha * obj.secL;
%                 maxY = (1-alpha) * obj.secL;
%                 minZ = (alpha-1) * obj.secH;
%                 maxZ = (1-alpha) * obj.secH;
%                 lb = [minX; minY; minZ];
%                 ub = [maxX; maxY; maxZ];
%                 pf = lb + rand(3,1) .* (ub-lb);
                % final position at the far right, midle in y and z
                pf = [0.9*obj.secW; obj.secL/2; 0];
                % unit vector in the direction of movement
                vUnit = (pf-pi)/norm(pf-pi,2);
                % absolute values of the initial velocities
                vnom = obj.aircraft{i}.getVnom();
                vxy = vnom * vUnit(1:2);
                timeI2F = norm(pf(1:2)-pi(1:2),2) / vnom;
                vz = (pf(3) - pi(3)) / timeI2F;
                v0 = [vxy; vz];
                vf = v0;
                % propagate backwards until reaching the initial position
                % at the boundary of the sector
                alpha = 0.0;
                minX = alpha * obj.secW;
                maxX = (1-alpha) * obj.secW;
                minY = alpha * obj.secL;
                maxY = (1-alpha) * obj.secL;
                minZ = (alpha-1) * obj.secH;
                maxZ = (1-alpha) * obj.secH;
                timeX = max((pf(1)-minX)/vxy(1),(pf(1)-maxX)/vxy(1));
                timeY = max((pf(2)-minY)/vxy(2),(pf(2)-maxY)/vxy(2));
                timeZ = max((pf(3)-minZ)/vz,(pf(3)-maxZ)/vz);
                timeSec = min([timeX,timeY,timeZ]);
                p0 = pf - v0 * timeSec;
                obj.aircraft{i}.setInitFinal(p0,pf,pi,v0,vf)
                % set reference trajectory
                obj.setRefTrajAC(i);
%                 vminH = vlim(1);
%                 vmaxH = vlim(2);
%                 vminV = vlim(3);
%                 vmaxV = vlim(4);
%                 vlb = [vminH; vminV];
%                 vub = [vmaxH; vmaxV];
%                 v0abs = vlb + rand(2,1) .* (vub - vlb);
             else
                % intermediate in a paralelepiped around A/C 1
                minX = -obj.horSep / sqrt(2);
                maxX =  obj.horSep / sqrt(2);
                minY = -obj.horSep / sqrt(2);
                maxY =  obj.horSep / sqrt(2);
                minZ = -obj.verSep;
                maxZ =  obj.verSep;
                lb = [minX; minY; minZ];
                ub = [maxX; maxY; maxZ];
                pi = lb + rand(3,1) .* (ub-lb) + obj.aircraft{1}.getPi();
                % final position anywhere in the sector
                alpha = 0;
                minX = alpha * obj.secW;
                maxX = (1-alpha) * obj.secW;
                minY = alpha * obj.secL;
                maxY = (1-alpha) * obj.secL;
                minZ = (alpha-1) * obj.secH;
                maxZ = (1-alpha) * obj.secH;
                lb = [minX; minY; minZ];
                ub = [maxX; maxY; maxZ];
                pf = lb + rand(3,1) .* (ub-lb);
                % unit vector in the direction of movement
                vUnit = (pf-pi)/norm(pf-pi,2);
                % absolute values of the initial velocities
                vnom = obj.aircraft{i}.getVnom();
                vxy = vnom * vUnit(1:2);
                timeI2F = norm(pf(1:2)-pi(1:2),2) / vnom;
                vz = (pf(3) - pi(3)) / timeI2F;
                v0 = [vxy; vz];
                vf = v0;
                % propagate backwards until reaching the initial position
                % at the boundary of the sector
                alpha = 0.0;
                minX = alpha * obj.secW;
                maxX = (1-alpha) * obj.secW;
                minY = alpha * obj.secL;
                maxY = (1-alpha) * obj.secL;
                minZ = (alpha-1) * obj.secH;
                maxZ = (1-alpha) * obj.secH;
                timeX = max((pf(1)-minX)/vxy(1),(pf(1)-maxX)/vxy(1));
                timeY = max((pf(2)-minY)/vxy(2),(pf(2)-maxY)/vxy(2));
                timeZ = max((pf(3)-minZ)/vz,(pf(3)-maxZ)/vz);
                timeSec = min([timeX,timeY,timeZ]);
                p0 = pf - v0 * timeSec;
                obj.aircraft{i}.setInitFinal(p0,pf,pi,v0,vf)
                % set reference trajectory
                obj.setRefTrajAC(i);
%                 vminH = vlim(1);
%                 vmaxH = vlim(2);
%                 vminV = vlim(3);
%                 vmaxV = vlim(4);
%                 vlb = [vminH; vminV];
%                 vub = [vmaxH; vmaxV];
%                 v0abs = vlb + rand(2,1) .* (vub - vlb);
             end
         end
      end
      function obj = setInitFinalAC(obj,p0,pf,pi,v0,vf)
        ac = obj.aircraft(index);
        ac.setInitFinal(p0,pf,pi,v0,vf);
      end
      function obj = setRefTrajAC(obj,index)
        ac = obj.aircraft{index};
        avgV = (ac.vf + ac.v0)/2;
        pLen = norm(ac.pf - ac.p0,2);
        timeSec = pLen / norm(avgV,2);
        avgAcc = (ac.vf - ac.v0) / timeSec;
        aux = linspace(0,1,obj.Nt);
        refV = ac.v0+ aux.*(ac.vf - ac.v0);
%         timeVec = ([0:1:obj.Nt])' * obj.dt;
%         refP = repmat(ac.p0,obj.Nt+1,1) + kron(timeVec ,ac.v0) + kron(timeVec.^2,avgAcc / 2);
        timeVec = ([0:1:obj.Nt]) * obj.dt;
        refP = repmat(ac.p0,1,obj.Nt+1) + kron(timeVec ,ac.v0) + kron(timeVec.^2,avgAcc / 2);
        ac.setRefTraj(refP,refV,timeSec);
      end
      function obj = plot(obj)
          figure;
          hold on;
          h = zeros(obj.Na,1);
          for i = 1:obj.Na
             refP = obj.aircraft{i}.getRefP();
             h(i) = plot3(refP(1,:),refP(2,:),refP(3,:),'*-');
             p0 = obj.aircraft{i}.getP0();
             pi = obj.aircraft{i}.getPi();
             pf = obj.aircraft{i}.getPf();
             plot3(p0(1),p0(2),p0(3),'o');
             plot3(pi(1),pi(2),pi(3),'+k');
             plot3(pf(1),pf(2),pf(3),'s');
             plotCylinderWithCaps(obj.horSep/2,pi-[0;0;obj.verSep/2],obj.verSep,20,[1,0,0],0.1);
             axis([0 obj.secW 0 obj.secL -obj.secH obj.secH]);
             axis square;
          end
          grid;
          xlabel('$x$ (NM)','interpreter','latex');
          ylabel('$y$ (NM)','interpreter','latex');
          zlabel('$z$ (kft)','interpreter','latex');
          legend(h,'A\C 1','A\C 2');
          hold off;
          view(3);
      end
      function windStr = getWindSpeed(obj)
          windStr = obj.windStr;
      end
   end
end