function [ res_madj remain_idx_vec ] = remove_sink_source_node( madj )
%REMOVE_SINK_SOURCE_NODE remove sink and source only nodes
%   
% \param[in] madj adjacency matrix
% \return res_madj sink and source node removed madj
%         remained_idx_vec remaining element idx vector
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[nr, nc] = size(madj);

remain_idx_vec = [1:nr];
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
sink_node_idx   = find(sum(madj') == 0);
madj(:, sink_node_idx) = [];
madj(sink_node_idx, :) = [];
remain_idx_vec(sink_node_idx) = [];

res_madj = madj
