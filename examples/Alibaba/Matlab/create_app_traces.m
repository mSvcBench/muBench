function [app_traces] = create_app_traces(v_G_app,u_traceids_a,sanitized_traces)
    % v_G_app{i} graph of app #i
    % u_traceids_a service of app #i
    % Alibaba sanitized traces
    % app_traces{i} is a table that contains the subset of traces of the app #i
    
    app_traces=cell(length(v_G_app),1);
    for i=1:length(v_G_app)
        app_traces{i} = table();
        for j=1:length(u_traceids_a{i})
            traceid = u_traceids_a{i}(j);
            trace_id_idx_1 = find(strcmp(sanitized_traces.traceid,traceid)>0);
            app_traces{i,:} = [app_traces{i,:};sanitized_traces(trace_id_idx_1,:)];
        end

        % trace/app check
        ms = unique([app_traces{i}.um ; app_traces{i}.dm]);
        if (length(ms)-1 ~= v_G_app{i}.numnodes)
            disp('Warning trace %d not consistent with app graph',i);
        end
        
    end
end