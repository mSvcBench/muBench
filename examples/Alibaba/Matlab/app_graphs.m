
function [v_G_app,u_services_a,u_traceids_a] = app_graphs(v_G_serv,u_services,u_traceids,sharingT,napps)
    % an app is a set of "similar" services. Grouping performed according to the paper https://ieeexplore.ieee.org/abstract/document/9774016 
    % v_G_app{i} dependency graph of app #i
    % u_service_a{i} set of services that belongs to app #i
    % u_traceids_a{i} set of traces that belongs to app #i
    % v_G_serv{i} dependency graph of service{i}
    % u_services{i} service name of service #i
    % u_traceids{i} set of traces of service #i
    % sharingT sharing threshold to declare two services as similar
    % napps number of applications to be generated, if <=0 then this number is computed as in the paper 
    
    
    s_Matrix = zeros(length(u_services),length(u_services));
    for i = 1:length(v_G_serv)
        service1 = u_services{i};
        nodes1= v_G_serv{i}.Nodes.Name;
        for j = i+1:length(v_G_serv)
            nodes2= v_G_serv{j}.Nodes.Name;
            service2 = u_services{j};
            common = sum(ismember(nodes1,nodes2));
            %fprintf("%d, %d common %d\n",i,j,common);
            if(common>sharingT*length(nodes1) && common>sharingT*length(nodes2))
              s_Matrix(i,j)=1;
              s_Matrix(j,i)=1;
            end
        end
    end
    % clustering for findings apps
    myfunc=@(X,K)(spectralcluster(X,K));
    if napps<=0
        k_opt=evalclusters(s_Matrix,myfunc,'CalinskiHarabasz','klist',2:50);
        napps = k_opt.OptimalK;
    end
    clusters = spectralcluster(s_Matrix,napps);
    v_G_app = {};
    for i=1:napps
        service_idx=find(clusters==i); %services idx of the cluster/app 
        v_G_app{i} = digraph();
        u_traceids_a{i} = strings(0);
        u_services_a{i} = strings(0);
        for j=1:length(service_idx)
            v_G_app{i} = addedge(v_G_app{i},v_G_serv{service_idx(j)}.Edges);
            u_traceids_a{i} = [u_traceids_a{i};u_traceids{service_idx(j)}];
            u_services_a{i} = [u_services_a{i}; u_services{i}];
        end
    end
end

        
    
    