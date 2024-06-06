function mb_trace_stats = create_app_traces_for_mbench(app_traces,dir_name,parallel)
% app_trace{i} traces concerning the i-th app
% for each app on app_traces, create a directory with JSON files of traces and a service_graph.json that can be used by µBench
% entry_service_id: dm microservice id called by the user, this value is specified below
% parallel = 1 means that a microservice carryout parallels calls to downstream microservices 
% mb_trace_stats{i} is a struct containing statistics (only length) of the traces of the i-th app 

mb_trace_stats = {};
entry_service_id = {'7695b43b41732a0f15d3799c8eed2852665fe8da29fd700c383550fc16e521a3'};
mkdir(dir_name);
for t=2:length(app_traces)
%for t=5:5
    app_trace = app_traces{t};
    app_trace_dir = "app"+num2str(t);
    mkdir(dir_name+"/"+app_trace_dir);
    names_map = unique([app_trace.um ; app_trace.dm]);
    names_map = names_map(2:end); % first row is for the user
    idx = find(strcmp(entry_service_id,names_map)>0);
    names_map=[entry_service_id;names_map(1:idx-1);names_map(idx+1:end)];
    
    tracesidx = unique(app_trace.traceid);
    
    % create a dummy service_graph.json file to be used with workmodel generator
    % and traces
    js = "{";
    for i = 1:length(names_map)
        js = js + char(34) + "s"+num2str(i-1)+char(34)+": {";
        js = js + char(34)+"external_services"+char(34)+": [{";
        js = js + char(34)+"seq_len"+char(34)+": 10000,";
        js = js + char(34)+"services"+char(34)+": []}]}";
        if i~=length(names_map)
            js = js + ",";
        end
    end
    js = js + "}";
    js = prettyjson(js);
    fid = fopen(dir_name+"/"+app_trace_dir+"/service_graph.json",'w');
    fprintf(fid,"%s",js);
    fclose(fid);
    
    for i = 1:length(tracesidx)
        single_trace = app_trace(find(strcmp(app_trace.traceid,tracesidx(i))>0),:);
        js="{";
        js = js+get_json_mubench('0.1',single_trace,names_map,parallel);
        %js = prettyjson(js);
        js=js+"}";
        fid = fopen(dir_name+"/"+app_trace_dir+"/trace"+num2str(i, '%0.5d')+".json",'w');
        fprintf(fid,"%s",js);
        fclose(fid);
        mb_trace_stats{t}.len(i) = height(single_trace)-1;
    end 
 end    
end