function [h1, h2, h3] = plotCylinderWithCaps(r,cnt,height,nSides,color,alpha)
[X,Y,Z] = cylinder(r,nSides);
X = X + cnt(1);
Y = Y + cnt(2);
Z = Z * height + cnt(3);
h1 = surf(X,Y,Z,'facecolor',color,'LineStyle','none','facealpha',alpha);
h2 = fill3(X(1,:),Y(1,:),Z(1,:),color,'facealpha',alpha);
h3 = fill3(X(2,:),Y(2,:),Z(2,:),color,'facealpha',alpha);
end  %only needed if this is within a script