%TEST_FIND_ZERO_COLUMN_VECTOR 
% Copyright (C) 2012 Hitoshi Yamauchi. Sunday Research
%
madj1 = [0 1 0 0 0;
         0 0 1 0 0;
         0 0 0 1 0;
         0 1 1 0 0;
         0 0 0 0 0];

madj2 = sparse(5,5);
madj2(1,2) = 1;
madj2(4,2) = 1;
madj2(2,3) = 1;
madj2(4,3) = 1;
madj2(3,4) = 1;

% madj1 and madj2 are the same.
% full(madj2) == madj1

madj = madj2;

[nr, nc] = size(madj);
zero_indices = find_zero_column_vector(madj);
% remove zero vectors
madj(:, zero_indices) = [];
madj(zero_indices, :) = [];
remain_vec = [1:nr]';
remain_vec(zero_indices) = [];
madj
remain_vec
pagerank(madj)
