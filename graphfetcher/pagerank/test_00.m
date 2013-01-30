%TEST_00 simple matrix pagerank test 
%   7x7 matrix pagerank test
clear;
madj = [0, 1, 1, 1, 1, 0, 1;
        1, 0, 0, 0, 0, 0, 0;
        1, 1, 0, 0, 0, 0, 0;
        0, 1, 1, 0, 1, 0, 0;
        1, 0, 1, 1, 0, 1, 0;
        1, 0, 0, 0, 1, 0, 0;
        0, 0, 0, 0, 1, 0, 0];
    
pagerank_vec = pagerank00(madj')

if(sum(pagerank_vec) < 0)
    % eigen vector can be any multiplication of a scalar
    pagerank_vec = -1 * pagerank_vec;
end

%  0.303514
%  0.166134
%  0.140575
%  0.105431
%  0.178914
%  0.044728
%  0.060703

% TODO test this matrix with some sink and source node
