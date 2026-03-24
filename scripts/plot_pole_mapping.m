%% plot_pole_mapping.m
%  Visualize hexapole pole tips and axes from filled/Hexapole_Assembly.STEP
%  Shows paper naming P1-P6 with OCP traversal index mapping.

clear; clc; close all;

%% Data extracted from filled/Hexapole_Assembly.STEP via CadQuery/OCP
%  Format: apex [x,y,z] mm, axis [dx,dy,dz] unit vector, OCP traversal index

% Lower plane (axis_z > 0)
P1_apex = [-41.2743, -82.8834, -18.0268];
P1_axis = [ 0.710371,  0.407901,  0.573576];
P1_ocp  = 5;

P3_apex = [-41.6187, -83.6539, -17.9249];
P3_axis = [-0.001600, -0.819150,  0.573576];
P3_ocp  = 6;

P6_apex = [-41.8643, -82.9396, -18.1050];
P6_axis = [-0.708756,  0.410700,  0.573576];
P6_ocp  = 4;

% Upper plane (axis_z < 0)
P2_apex = [-41.8734, -83.2489, -18.7044];
P2_axis = [-0.862698, -0.495835, -0.099504];
P2_ocp  = 3;

P4_apex = [-41.6172, -82.8751, -18.6976];
P4_axis = [ 0.001943,  0.995035, -0.099504];
P4_ocp  = 1;

P5_apex = [-41.3628, -83.2497, -18.7044];
P5_axis = [ 0.860754, -0.499201, -0.099504];
P5_ocp  = 2;

%% Collect into arrays
names  = {'P1','P2','P3','P4','P5','P6'};
apexes = [P1_apex; P2_apex; P3_apex; P4_apex; P5_apex; P6_apex];
axes   = [P1_axis; P2_axis; P3_axis; P4_axis; P5_axis; P6_axis];
ocp_idx = [P1_ocp, P2_ocp, P3_ocp, P4_ocp, P5_ocp, P6_ocp];
pairs  = {[1,2], [3,4], [5,6]};  % P1-P2, P3-P4, P5-P6

% Colors: lower=red, upper=blue
colors = [1 0 0;   % P1 lower
          0 0 1;   % P2 upper
          1 0 0;   % P3 lower
          0 0 1;   % P4 upper
          0 0 1;   % P5 upper
          1 0 0];  % P6 lower

pair_colors = [0.8 0.2 0.2;    % P1-P2
               0.2 0.7 0.2;    % P3-P4
               0.2 0.2 0.8];   % P5-P6

arrow_len = 0.4;  % axis arrow length in mm

%% Figure 1: 3D view
figure('Name', 'Hexapole Pole Mapping (3D)', 'Position', [100 100 800 700]);
hold on; grid on; axis equal;

% Plot pole tips and axes
for i = 1:6
    % Tip point
    plot3(apexes(i,1), apexes(i,2), apexes(i,3), 'o', ...
        'MarkerSize', 10, 'MarkerFaceColor', colors(i,:), ...
        'MarkerEdgeColor', 'k', 'LineWidth', 1.5);

    % Axis arrow
    quiver3(apexes(i,1), apexes(i,2), apexes(i,3), ...
        axes(i,1)*arrow_len, axes(i,2)*arrow_len, axes(i,3)*arrow_len, ...
        0, 'Color', colors(i,:), 'LineWidth', 2, 'MaxHeadSize', 0.5);

    % Label: "P# (OCP #)"
    label = sprintf('%s (OCP %d)', names{i}, ocp_idx(i));
    text(apexes(i,1), apexes(i,2), apexes(i,3) + 0.08, label, ...
        'FontSize', 11, 'FontWeight', 'bold', 'Color', colors(i,:), ...
        'HorizontalAlignment', 'center');
end

% Draw pair connecting lines
pair_names = {'P1\leftrightarrowP2', 'P3\leftrightarrowP4', 'P5\leftrightarrowP6'};
for k = 1:3
    idx = pairs{k};
    i = idx(1); j = idx(2);
    dist = norm(apexes(j,:) - apexes(i,:));
    mid = (apexes(i,:) + apexes(j,:)) / 2;

    plot3([apexes(i,1) apexes(j,1)], ...
          [apexes(i,2) apexes(j,2)], ...
          [apexes(i,3) apexes(j,3)], ...
          '--', 'Color', pair_colors(k,:), 'LineWidth', 2);

    text(mid(1), mid(2), mid(3) - 0.1, ...
        sprintf('%s\n%.4f mm', pair_names{k}, dist), ...
        'FontSize', 9, 'Color', pair_colors(k,:), ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold');
end

xlabel('X (mm)'); ylabel('Y (mm)'); zlabel('Z (mm)');
title('Hexapole Pole Tip Mapping: Paper P1-P6 vs OCP Index');
legend_entries = {'Lower plane (P1,P3,P6)', 'Upper plane (P2,P4,P5)'};
h1 = plot3(nan,nan,nan,'or','MarkerFaceColor','r','MarkerSize',10);
h2 = plot3(nan,nan,nan,'ob','MarkerFaceColor','b','MarkerSize',10);
legend([h1 h2], legend_entries, 'Location', 'best', 'FontSize', 10);
view(30, 25);
hold off;

%% Figure 2: Top-down XY view (clearer for hexapole layout)
figure('Name', 'Hexapole Pole Mapping (Top View)', 'Position', [950 100 700 650]);
hold on; grid on; axis equal;

for i = 1:6
    plot(apexes(i,1), apexes(i,2), 'o', ...
        'MarkerSize', 14, 'MarkerFaceColor', colors(i,:), ...
        'MarkerEdgeColor', 'k', 'LineWidth', 1.5);

    % Axis arrow (XY projection)
    quiver(apexes(i,1), apexes(i,2), ...
        axes(i,1)*arrow_len, axes(i,2)*arrow_len, ...
        0, 'Color', colors(i,:), 'LineWidth', 2.5, 'MaxHeadSize', 0.8);

    label = sprintf('%s\n(OCP %d)', names{i}, ocp_idx(i));
    offset_y = 0.12;
    if axes(i,2) > 0
        offset_y = 0.12;
    else
        offset_y = -0.15;
    end
    text(apexes(i,1), apexes(i,2) + offset_y, label, ...
        'FontSize', 12, 'FontWeight', 'bold', 'Color', colors(i,:), ...
        'HorizontalAlignment', 'center');
end

% Pair lines
for k = 1:3
    idx = pairs{k};
    i = idx(1); j = idx(2);
    dist = norm(apexes(j,:) - apexes(i,:));
    mid = (apexes(i,:) + apexes(j,:)) / 2;

    plot([apexes(i,1) apexes(j,1)], ...
         [apexes(i,2) apexes(j,2)], ...
         '--', 'Color', pair_colors(k,:), 'LineWidth', 2);

    text(mid(1) + 0.15, mid(2), sprintf('%.4f mm', dist), ...
        'FontSize', 10, 'Color', pair_colors(k,:), 'FontWeight', 'bold');
end

xlabel('X (mm)'); ylabel('Y (mm)');
title('Hexapole Top View: Paper P1-P6 vs OCP Index');
subtitle('Red = Lower plane, Blue = Upper plane, Arrows = axis direction (XY projection)');
h1 = plot(nan,nan,'or','MarkerFaceColor','r','MarkerSize',12);
h2 = plot(nan,nan,'ob','MarkerFaceColor','b','MarkerSize',12);
legend([h1 h2], {'Lower (P1,P3,P6)','Upper (P2,P4,P5)'}, ...
    'Location', 'best', 'FontSize', 10);
hold off;

%% Print summary
fprintf('\n=== Pole Mapping Summary ===\n');
fprintf('%-4s  %-6s  %-8s  Apex (mm)\n', 'Name', 'Plane', 'OCP Idx');
fprintf('%s\n', repmat('-', 1, 55));
for i = 1:6
    if axes(i,3) > 0
        plane = 'Lower';
    else
        plane = 'Upper';
    end
    fprintf('%-4s  %-6s  OCP %-3d   (%+.4f, %+.4f, %+.4f)\n', ...
        names{i}, plane, ocp_idx(i), apexes(i,1), apexes(i,2), apexes(i,3));
end

fprintf('\n=== Opposing Pairs ===\n');
for k = 1:3
    idx = pairs{k};
    i = idx(1); j = idx(2);
    dist = norm(apexes(j,:) - apexes(i,:));
    dot_val = dot(axes(i,:), axes(j,:));
    fprintf('%s <-> %s : tip-to-tip = %.4f mm, dot = %.4f\n', ...
        names{i}, names{j}, dist, dot_val);
end

%% Save figures
out_dir = fileparts(mfilename('fullpath'));

fig_list = findobj('Type', 'figure');
for f = 1:numel(fig_list)
    fig = fig_list(f);
    fig_name = get(fig, 'Name');
    if contains(fig_name, '3D')
        exportgraphics(fig, fullfile(out_dir, 'pole_mapping_3d.png'), 'Resolution', 200);
        fprintf('Saved: pole_mapping_3d.png\n');
    elseif contains(fig_name, 'Top')
        exportgraphics(fig, fullfile(out_dir, 'pole_mapping_top.png'), 'Resolution', 200);
        fprintf('Saved: pole_mapping_top.png\n');
    end
end
