% Plot illustrative LOS
% Prof. Rubens J M Afonso
close all;

horSep = 5; % horizontal separation [NM]
verSep = 1; % vertical separation [kft]
Na = 2; % number of A/C
secW = 30; % sector width [NM]
secL = 30; % sector length [NM]
secH = 4; % sector height [kft]
Nt = 12; % number of time steps
dt = 0.5; % sample time [min]

% build scenario
scen = LOSScenario(horSep,verSep,Na,secW,secL,secH,Nt,dt);
% ATCO advisory
Maneuver = atco_label(scen)
% plot scenario
scen.plot();

print -depsc2 -r300 IllustrativeLOS
