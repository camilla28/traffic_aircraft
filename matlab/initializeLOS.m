% Initialize LOS scenario
% Prof. Rubens J M Afonso

horSep = 5; % horizontal separation [NM]
verSep = 1; % vertical separation [kft]
Na = 2; % number of A/C
secW = 30; % sector width [NM]
secL = 30; % sector length [NM]
secH = 4; % sector height [kft]
Nt = 12; % number of time steps
dt = 0.5; % sample time [min]





Ns = 500;
% Create Ns scenarios
scen = cell(Ns,1);
modelA = [];
modelB = [];
x0A = [];
y0A = [];
z0A = [];
x0B = [];
y0B = [];
z0B = [];
xfA = [];
yfA = [];
zfA = [];
xfB = [];
yfB = [];
zfB = [];
timeA = [];
timeB = [];
companyA = [];
companyB = [];
WindSpeed = [];
Maneuver = cell(Ns,1);
for i = 1:Ns
    scen{i} = LOSScenario(horSep,verSep,Na,secW,secL,secH,Nt,dt);
    % ATCO advisory
    Maneuver{i} = atco_label(scen{i});
    
    modelA = [modelA; scen{i}.aircraft{1}.getAcType()];
    modelB = [modelB; scen{i}.aircraft{2}.getAcType()];
    
    p0A = scen{i}.aircraft{1}.getP0();
    p0B = scen{i}.aircraft{2}.getP0();
    x0A = [x0A; p0A(1)];
    y0A = [y0A; p0A(2)];
    z0A = [z0A; p0A(3)];
    x0B = [x0B; p0B(1)];
    y0B = [y0B; p0B(2)];
    z0B = [z0B; p0B(3)];
    
    pfA = scen{i}.aircraft{1}.getPf();
    pfB = scen{i}.aircraft{2}.getPf();
    xfA = [xfA; pfA(1)];
    yfA = [yfA; pfA(2)];
    zfA = [zfA; pfA(3)];
    xfB = [xfB; pfB(1)];
    yfB = [yfB; pfB(2)];
    zfB = [zfB; pfB(3)];
    
    timeA = [timeA; scen{i}.aircraft{1}.getTimeSec()];
    timeB = [timeB; scen{i}.aircraft{2}.getTimeSec()];
    
    companyA = [companyA; scen{i}.aircraft{1}.getCompany()];
    companyB = [companyB; scen{i}.aircraft{2}.getCompany()];
    WindSpeed = [WindSpeed;scen{i}.getWindSpeed()];
end
% scen.plot();
labels = {'A/C model A', 'A/C model B', 'x0 A', 'x0 B', 'y0 A', 'y0 B',...
    'z0 A', 'z0 B', 'xf A', 'xf B', 'yf A', 'yf B', 'zf A', 'zf B',...
    'Time A', 'Time B', 'Company A', 'Company B', 'Wind speed','Maneuver'};
% LastName = {'Smith';'Johnson';'Williams';'Jones';'Brown'};
% Age = [38;43;38;40;49];
% Height = [71;69;64;67;64];
% Weight = [176;163;131;133;119];
% BloodPressure = [124 93; 109 77; 125 83; 117 75; 122 80];
%
T = table(modelA, modelB, x0A, x0B, y0A, y0B, z0A, z0B, ...
xfA, xfB, yfA, yfB, zfA, zfB, timeA, timeB, companyA, companyB, ...
WindSpeed,Maneuver);
writetable(T);