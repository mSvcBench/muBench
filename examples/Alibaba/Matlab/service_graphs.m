function [v_G_serv,u_services,u_traceids] = service_graphs(sanitized_traces)
    % v_G_serv{i} is the graph of a service where a service is identified by the interface name of the first call
    % u_services{i} interface name of the service i-th
    % u_traceids{i} set of traceids that regards service i-th
    % sanitized_trace, Alibaba trace sanitized 
    
    v_G_serv = {}; % graphs of services, a service is identified by the interface name of the first call
    trace_id_idx_1 = find(strcmp(sanitized_traces.rpcid,"0")>0);
    services = cell(sanitized_traces.interface(trace_id_idx_1));
    trace_ids = cell(sanitized_traces.traceid(trace_id_idx_1));
    u_services = unique(services);  % unique service id
    u_traceids = cell(length(u_services),1); % trace id of the services
    for i=1:length(u_services)
        u_traceids{i} = strings(0);
        v_G_serv{i} = digraph();
    end
    l = length(trace_ids);
    for i = 1:l
        service = services{i};
        traceid = trace_ids{i};
        trace_id_idx_1 = find(strcmp(sanitized_traces.traceid,traceid)>0);
        trace_g = sanitized_traces(trace_id_idx_1,:);
        u_service_id = find(strcmp(u_services,service),1,'first');
        u_traceids{u_service_id} = [u_traceids{u_service_id}; traceid];
        for j = 1 : height(trace_g)
            
            % add um,dm nodes
            if strcmp(trace_g.rpcid{j},'0')
                continue
            end
            um = trace_g.um{j};
            dm = trace_g.dm{j};
            % add nodes
            if numnodes(v_G_serv{u_service_id})==0
                v_G_serv{u_service_id} = addnode(v_G_serv{u_service_id},um);
            elseif not(findnode(v_G_serv{u_service_id},um))
                v_G_serv{u_service_id} = addnode(v_G_serv{u_service_id},um);
            end
            if not(findnode(v_G_serv{u_service_id},dm))
                v_G_serv{u_service_id} = addnode(v_G_serv{u_service_id},dm);
            end
            % add edges
            v_G_serv{u_service_id} = addedge(v_G_serv{u_service_id},um,dm); % add one edge x call
%             if strcmp(um,dm)
%                 %skip autocall
%                 continue
%             end
%             if findedge(v_G_serv{u_service_id},um,dm) == 0
%                 v_G_serv{u_service_id} = addedge(v_G_serv{u_service_id},um,dm); % add one edge x call
%             end
        end
    end
end
    
    