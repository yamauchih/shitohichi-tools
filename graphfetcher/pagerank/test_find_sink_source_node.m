%TEST_FIND_SINK_OR_SOURCE_NODE 
% Copyright (C) 2012 Hitoshi Yamauchi. Sunday Research
%
madj1 = [0 1 0 0 0;
         0 0 1 0 0;
         0 0 0 1 0;
         0 1 1 0 1;
         0 0 0 0 0];

madj2 = sparse(5,5);
madj2(1,2) = 1;
madj2(4,2) = 1;
madj2(2,3) = 1;
madj2(4,3) = 1;
madj2(3,4) = 1;
madj2(4,5) = 1;


% madj1 and madj2 are the same.
% full(madj2) == madj1

madj = madj2;

% [nr, nc] = size(madj);
% remain_vec = [1:nr];
% source_node_idx = find(sum(madj)  == 0);
% madj(:, source_node_idx) = [];
% madj(source_node_idx, :) = [];
% remain_vec(source_node_idx) = [];
% 
% sink_node_idx   = find(sum(madj') == 0);
% madj(:, sink_node_idx) = [];
% madj(sink_node_idx, :) = [];
% remain_vec(sink_node_idx) = [];

[simplified_madj remain_idx_vec]= remove_sink_source_node(madj)

full(madj)
full(simplified_madj)
remain_idx_vec
pagerank(simplified_madj)
