%TEST_FIND_ONE_INPUT_NODE 
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

[nr, nc] = size(madj);
one_indices = find_one_input_node(madj);
% remove 1-nonzero vectors
madj(:, one_indices) = [];
madj(one_indices, :) = [];
remain_vec = [1:nr]';
remain_vec(one_indices) = [];
madj
remain_vec
% pagerank(madj)
