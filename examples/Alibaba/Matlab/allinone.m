% all-in-one script to create app and app trace for µBench starting from
% Alibaba MSCallGraph (https://github.com/alibaba/clusterdata/blob/master/cluster-trace-microservices-v2021/README.md)

alibaba_trace = "MSCallGraph_0.csv";
callg=readtable(alibaba_trace);

% extract 20000 complete traces
[sanitized_traces,v_G_sub] = trace_sanity(callg,20000)

% extract services
[v_G_serv,u_services,u_traceids] = service_graphs(sanitized_traces);

% extract 30 apps
[v_G_app,u_services_a,u_traceids_a] = app_graphs(v_G_serv,u_services,u_traceids,0.2,30);

% group traces of apps
[app_traces] = create_app_traces(v_G_app,u_traceids_a,sanitized_traces);

% create mubench traces sequential
mb_trace_stats_seq = create_app_traces_for_mbench(app_traces,"traces-mbench/seq",0);

% create mubench traces parallel
mb_trace_stats_par = create_app_traces_for_mbench(app_traces,"traces-mbench/par",1);

