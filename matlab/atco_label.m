% Solve LOS maneuvers as an ATCO
% Prof. Rubens J M Afonso
function maneuver = atco_label(scenario)
maneuver = [];
% separate horizontally if wind is too strong
% rationale: climb/descent uncertain
if scenario.windStr > 40
    maneuver = 'PATHSEP';
elseif scenario.windStr > 30
    maneuver = 'SEPHORIZ';
else
    
    % get expected time to pf
    time1 = scenario.aircraft{1}.getTimeSec();
    time2 = scenario.aircraft{2}.getTimeSec();
    % the one that has more time to the target goes behind
    % rationale: more time to recover lost time and fast A/C
    if time1 > 1.2*time2 && scenario.aircraft{1}.acType == 1
        maneuver = 'BEFORE(2,1)';
    elseif time2 > 1.2*time1 && scenario.aircraft{2}.acType == 1
        maneuver = 'BEFORE(1,2)';
    end
    
    % if expected time to target < 4 time steps, than maintain path
    if time1 < 4*scenario.dt
        maneuver = 'FIXPATH(1)';
    elseif time2 < 4*scenario.dt
        maneuver = 'FIXPATH(2)';
    end
    
    % in case none of the above was selected
    if isempty(maneuver)
        % get final position of each aircraft
        pf1 = scenario.aircraft{1}.getPf();
        pf2 = scenario.aircraft{2}.getPf();
        % the one that finishes higher flies above
        if pf1(3) > pf2(3)
            maneuver = 'OVER(1,2)';
        else
            maneuver = 'OVER(2,1)';
        end
    end
end
end