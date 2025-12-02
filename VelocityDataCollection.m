disp(serialportlist("available"));
% JOSH IMPORTANT NOTE
% SERIAL MONITOR MUST BE CLOSED FOR MATLAB TO COLLECT DATA

%% DATA COLLECTION

% ----------- USER SETTINGS -----------
portName = "COM9";     % change this to your Arduino port
baud = 115200;
recordSeconds = 70;    % how long to record
Fs = 119;              % sampling rate (Hz)
inactivityLimit = 8;
% -------------------------------------

s = serialport(portName, baud);
configureTerminator(s,"LF");
% flush(s);

% Preallocate (approx 119 Hz sampling)
Nmax = recordSeconds * 50;  % oversized for safety
time = zeros(Nmax,1);

vx = zeros(Nmax,1);
vy = zeros(Nmax,1);
vz = zeros(Nmax,1);
vt = zeros(Nmax,1);

vt_conc = zeros(Nmax,1); % Storing vector for only concentric vals

idx = 0;
tStart = tic;

figure;

% ---- Velocity Plots ----
hold on; grid on;
xlabel("Time (s)");
ylabel("Velocity (m/s)");
title("Real-Time Velocity");
h_vx = plot(0,0,'Color',[0.4 0.4 0.4]);
h_vy = plot(0,0,'Color',[0.4 0.4 0.4]);
h_vz = plot(0,0,'Color',[0.6 0.6 1]); % blue

h_vt = plot(0,0, 'Color', 'white'); % base Vt data
h_vt_conc = plot(0,0,'Color', 'r', 'LineWidth',2); % concentric overlay (red)

legend("vx","vy","vz","vt","concentric");

% -- Holding Concentric Info / Vars -- %
conc_thresh = -0.05;
rep_count = 1;
prev_conc = false;
rep_indices = zeros(25,2); % oversized for safety
rep_thresh = 0.3;

while toc(tStart) < recordSeconds
    raw = readline(s);
    parts = strsplit(strtrim(raw),',');

    % Expect 7 values: time, vx, vy, vz
    if numel(parts) ~= 4
        continue;
    end

    idx = idx + 1;

    time(idx) = str2double(parts{1}) / 1e6;

    vx(idx)   = str2double(parts{2});
    vy(idx)   = str2double(parts{3});
    vz(idx)   = str2double(parts{4});
    
    % Calculating total vel by taking rms 
    vt(idx) = sqrt(vx(idx)*vx(idx) + vy(idx)*vy(idx) + vz(idx)*vz(idx));

    % Concentric specific logic
    if vz(idx) < conc_thresh
        vt_conc(idx) = vt(idx); % Store concentric velocity values

        % Upon State switch, store the start idx
        if prev_conc == false
            rep_indices(rep_count, 1) = idx;
            prev_conc = true;
        end

    % Upon state switch to eccentric, store end idx
    else
        vt_conc(idx) = NaN;       % hide non-concentric


        if prev_conc == true
            prev_conc = false;
            rep_indices(rep_count,2) = idx;
    
            % Rep_Count will only increment upon a valid rep (> rep thresh)
            if (time(rep_indices(rep_count,2)) - time(rep_indices(rep_count,1))) > rep_thresh
                title("Real-Time Velocity | Reps Completed: " + rep_count);
                rep_count = rep_count + 1; % Increment the repetition count
            end
        end

        % Stop Data collection upon inactivity for certain amt of time
        if rep_count > 4
            if (time(idx) - time(rep_indices(rep_count-1,2))) > inactivityLimit
                break;
            end 
        end 
    end


    % Update plots every 5 samples (smooth real-time)
    if mod(idx,5) == 0

        % ---- Update Velocity Plot ----
        set(h_vx,'XData',time(1:idx),'YData',vx(1:idx));
        set(h_vy,'XData',time(1:idx),'YData',vy(1:idx));
        set(h_vz,'XData',time(1:idx),'YData',vz(1:idx));
        set(h_vt,'XData',time(1:idx),'YData',vt(1:idx));

        set(h_vt_conc,'XData',time(1:idx),'YData',vt_conc(1:idx));

        drawnow limitrate;
    end
end


% Trimming
time = time(1:idx);

vx = vx(1:idx); vy = vy(1:idx); vz = vz(1:idx); 
vt = vt(1:idx); vt_conc = vt_conc(1:idx);

rep_count = rep_count - 1;
rep_indices = rep_indices(1:rep_count,:);

disp("Done! Velocity Plotted!");
clear s;

% ============================
%      Displaying Rep Data
% =============================
avgVelocity = zeros(rep_count, 1);
startIdx = zeros(rep_count, 1);
endIdx = zeros(rep_count, 1);
duration = zeros(rep_count, 1);
peakVelocity = zeros(rep_count, 1);

for i = 1:rep_count
    startIdx(i) = rep_indices(i,1);
    endIdx(i) = rep_indices(i,2);
    duration(i) = time(endIdx(i)) - time(startIdx(i));

    avgVelocity(i) = mean(vt(startIdx(i):endIdx(i)));
    peakVelocity(i) = max(vt(startIdx(i):endIdx(i)));
end 

% Vel Loss calculation
velocityLoss = (avgVelocity(1) - avgVelocity(rep_count)); % start - end / start 
velocityLoss = velocityLoss * 100 / (avgVelocity(1));



% Plotting Rep Summaries
figure;
plot(avgVelocity, 'LineWidth', 1.5);
hold on;
plot(peakVelocity, 'LineWidth', 1.5);
hold on;
    % Peak Vel Slope Calculations
    peakVel_poly = polyfit(1:rep_count, peakVelocity, 1);
    plot((1:rep_count), polyval(peakVel_poly,1:rep_count), '-');
ylim([min(avgVelocity) - 0.25,max(peakVelocity) + 0.25]);
xlabel("Rep #");
ylabel("Velocity (m/s)");
title("Mean + Peak Velocity Change | Vel Loss: " + velocityLoss + "%");
legend('Mean Vel', "Peak Vel", "Peak Best Fit");
grid;
hold on;

%create a display a table of each rep window
repSummary = table( (1:rep_count)',duration, startIdx, endIdx, avgVelocity, peakVelocity, ...
    'VariableNames',{'Rep#', 'Duration (s)', 'StartIdx', 'EndIdx', 'Avg Vel', 'Peak Vel'});
disp(repSummary);

% --- Feature Extraction --- 
meanVel_loss = velocityLoss; % Already calculated 
meanVel_lastRep = avgVelocity(rep_count);
% rep_count
peakVel_slope = peakVel_poly(1);
setDuration = time(endIdx(rep_count)) - time(startIdx(1)); % start of first rep to end of last rep
concDuration = sum(duration); % total time during concentrics

% Displaying Features in Command
setFeatures = table(rep_count, meanVel_loss, meanVel_lastRep, peakVel_slope, setDuration, concDuration, ...
    'VariableNames',{'Rep Count', 'Vel Loss (%)', 'Last Rep Vel (m/s)','Peak Vel Slope', 'Total Set Duration (s)', 'Concentric Duration (s)'});
disp(setFeatures);


%%
repStart = 1; repEnd = 6;
peakVel_poly2 = polyfit(repStart:repEnd, peakVelocity(repStart:repEnd), 1);
disp("Peak vel at those reps: " + peakVel_poly2(1));