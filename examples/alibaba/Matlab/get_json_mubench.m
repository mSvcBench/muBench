function js = get_json_mubench(rpcid,app_trace,names_map,parallel)
idx = find(strcmp(app_trace.rpcid,rpcid)>0,1);
ms = app_trace.um{idx};
ms_id = find(strcmp(names_map,ms)>0,1)-1;
js = char(34)+"s"+num2str(ms_id)+"__"+num2str(randi([0 1e5]))+char(34)+":[";    
ms_id = find(strcmp(names_map,ms)>0,1)-1;
rpcid_child = convertCharsToStrings(rpcid)+".1";
if isempty(find(strcmp(app_trace.rpcid,rpcid_child)))
    child_id = find(strcmp(names_map,app_trace.dm{idx})>0,1)-1;
    js = char(34)+"s"+num2str(child_id)+"__"+num2str(randi([0 1e5]))+char(34)+":[{}]";
    return;
else
    if parallel~=1
        js = js + "{";
    end
    for i=1:1000
        %recursion on childs
        rpcid_child = convertCharsToStrings(rpcid)+"."+num2str(i);
        if isempty(find(strcmp(app_trace.rpcid,rpcid_child)))
            break
        else
            if parallel==1
                js = js + "{"+get_json_mubench(rpcid_child,app_trace,names_map,parallel)+"},";
            else    
                js = js + get_json_mubench(rpcid_child,app_trace,names_map,parallel)+",";            
            end
        end
    end
end
js = convertStringsToChars(js);
if (js(end)==',')
    js=js(1:end-1);
end
js = convertCharsToStrings(js);
if parallel~=1
    js = js + "}";
end
js = js + "]";
end