function [ res_madj remain_idx_vec remain_name_carray ] = ...
    remove_sink_source_node( madj, idx_vec, name_carray)
%REMOVE_SINK_SOURCE_NODE remove sink and source only nodes
%   
% \param[in] madj adjacency matrix
% \param[in] idx_vec index vector to keep track with which elements 
% are deleted 
% \param[in] name_carray name cell array to keep track with which names
% are deleted 
% \return res_madj sink and source node removed madj
%         remained_idx_vec remaining element idx vector
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[ir, ic] = size(idx_vec);
if ((ir ~= nr) || (ic ~= 1))
    error('idx_vec does not agree with madj size.')
end
[ir, ic] = size(name_carray);
if ((ir ~= nr) || (ic ~= 1))
    error('name_carray does not agree with madj size.')
end

iter = 0;
% Note: can not use find(X,1) since a sparce matrix is expected.
while ((~isempty(find(sum(madj') == 0))) || ...
       (~isempty(find(sum(madj)  == 0))))
    [ res_madj remain_idx_vec remain_name_carray ] = ...
        remove_sink_source_node_sub(madj, idx_vec, name_carray);
    % res_madj
    % remain_idx_vec
    % remain_name_carray
    madj = res_madj;
    idx_vec   = remain_idx_vec;
    name_carray = remain_name_carray;
    iter = iter + 1;
    [nr, nc] = size(madj);
    fprintf('remove_sink_source_node: %d iters. size(%d,%d)\n', iter, nr, nc);
end

end
%% subroutine of remove_sink_source_node.
function [sres_madj sremain_idx_vec sremain_name_carray] = ...
    remove_sink_source_node_sub(madj, idx_vec, name_carray)
% REMOVE_SINK_SOURCE_NODE_SUB
%
%
sremain_idx_vec = idx_vec;
sremain_name_carray = name_carray;
% remove source only nodes
% PageRank paper did not mention this. I think the reasons are:
%   1. numerically less problem compare to sink node
%   2. in the case of web, a node is referenced from anyone is harder
%      than a node is referring to others.
%
source_node_idx = find(sum(madj) == 0);
madj(:, source_node_idx) = [];
madj(source_node_idx, :) = [];
sremain_idx_vec(source_node_idx) = [];
sremain_name_carray(source_node_idx) = [];

% remove sink only nodes 
% (same as find(sum(madj') == 0), but no transpose needed.
sink_node_idx   = (find(sum(madj,2) == 0))';
madj(:, sink_node_idx) = [];
madj(sink_node_idx, :) = [];
sremain_idx_vec(sink_node_idx) = [];
sremain_name_carray(sink_node_idx) = [];

sres_madj = madj;

end
