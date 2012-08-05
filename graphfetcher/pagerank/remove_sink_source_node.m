function [ res_madj remain_idx_vec ] = remove_sink_source_node( madj, idx_vec)
%REMOVE_SINK_SOURCE_NODE remove sink and source only nodes
%   
% \param[in] idx_vec index vector to keep track with which elements 
% are deleted 
% \param[in] madj adjacency matrix
% \return res_madj sink and source node removed madj
%         remained_idx_vec remaining element idx vector
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[ir, ic] = size(idx_vec);
if ((ir ~= nr) || (ic ~= 1))
    error('idx_vec does not agree with madj size')
end

remain_idx_vec = idx_vec;
% remove source only nodes
% PageRank paper did not mention this. I think the reasons are:
%   1. numerically less problem compare to sink node
%   2. in the case of web, a node is referenced from anyone is harder
%      than a node is referring to others.
%
source_node_idx = find(sum(madj) == 0);
madj(:, source_node_idx) = [];
madj(source_node_idx, :) = [];
remain_idx_vec(source_node_idx) = [];

% remove sink only nodes 
% (same as find(sum(madj') == 0), but no transpose needed.
sink_node_idx   = (find(sum(madj,2) == 0))';
madj(:, sink_node_idx) = [];
madj(sink_node_idx, :) = [];
remain_idx_vec(sink_node_idx) = [];

res_madj = madj;
