function [ removed_idx_vec ] = find_sink_or_source_node( madj )
%FIND_SINK_OR_SOURCE_NODE find sink node or source node
%   find zero column|row vectors and return the indeces
%   
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[nr, nc] = size(madj);
removed_idx_vec = [];
% find zero vectors
for i = 1:nc
    % for sparse matrix find(X,k) is not possible
    if (isempty(find(madj(:,i))))
        removed_idx_vec = [removed_idx_vec i];
        continue
    end
    if (isempty(find(madj(i,:))))
        removed_idx_vec = [removed_idx_vec i];
    end
end
