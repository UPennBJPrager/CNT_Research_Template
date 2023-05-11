function ekg = find_non_ieeg(labels)

% ADD DC CHANNELS
%% Added 11/13, Haoer
% assume cell format of channel labels
if ~iscell(labels)
    try
        % convert to cell if table format
        if istable(labels)
            labels = table2cell(labels); 
        
        % convert to cell if string or char format
        elseif isstring(labels) || ischar(labels)
            labels = cellstr(labels); 
        end
    
    catch ME
        throw(MException('CNTtools:invalidInputType','Electrode labels should be a cell array.'))
    end
end
% end of added part

ekg = zeros(length(labels),1);

for i = 1:length(labels)
    
    if contains(labels(i),'ekg','ignorecase',true)
        ekg(i) = 1;
    end
    
    if contains(labels(i),'ecg','ignorecase',true)
        ekg(i) = 1;
    end
    
    if contains(labels(i),'rate','ignorecase',true)
        ekg(i) = 1;
    end
    
    if contains(labels(i),'rr','ignorecase',true)
        ekg(i) = 1;
    end
    
    if strcmp(labels(i),'C3') || strcmp(labels(i),'C4') || ...
            strcmp(labels(i),'CZ') || ...
            strcmp(labels(i),'F8') || ...
            strcmp(labels(i),'F7') || ...
            strcmp(labels(i),'F4') || ...
            strcmp(labels(i),'F3') || ...
            strcmp(labels(i),'FP2') || ...
            strcmp(labels(i),'FP1') || ...
            strcmp(labels(i),'Fp2') || ...
            strcmp(labels(i),'Fp1') || ...
            strcmp(labels(i),'FZ') || ...
            strcmp(labels(i),'LOC') || ...
            strcmp(labels(i),'T4') || ...
            strcmp(labels(i),'T5') || ...
            strcmp(labels(i),'T3') || ...
            strcmp(labels(i),'C6') || ...
            strcmp(labels(i),'ROC') || ...
            strcmp(labels(i),'P4') || ...
            strcmp(labels(i),'P3') || ...
            strcmp(labels(i),'T6') 
            

        ekg(i) = 1;
    end
    
    % fix for things that could be either scalp or ieeg
    %{
    if strcmp(labels(i),'O2') 
        if sum(strcmp(labels,'O1')) == 0 % if hemiscalp, should not have odd; if ieeg, should have O1
            ekg(i) = 1;
        end
    end
    %}
    
    if strcmp(labels(i),'O1') || strcmp(labels(i),'O2')
        if sum(strcmp(labels,'O3')) == 1 || sum(strcmp(labels,'O4')) == 1 % if intracranial, should have these too
            ekg(i) = 0;
        else
            ekg(i) = 1;
        end
    end

    
end

ekg = logical(ekg);

end