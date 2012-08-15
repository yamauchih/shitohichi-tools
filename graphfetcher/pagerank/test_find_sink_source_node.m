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
matsz = size(madj);

% all the indices are valid
index_vec = [1:matsz(1)]';

[simplified_madj remain_idx_vec]= remove_sink_source_node(madj, index_vec);

full(madj)
full(simplified_madj)
remain_idx_vec
pagerank(simplified_madj)
