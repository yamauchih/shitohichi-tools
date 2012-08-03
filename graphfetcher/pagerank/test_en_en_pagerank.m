%TEST_EN_EN_PAGERANK Summary of this function goes here
%   Detailed explanation goes here

en_en_writer_adj_mat_selected;

[nr, nc] = size(madj);
zero_idx_vec = find_zero_column_vector(madj);
remain_vec = [1:nr]';
% remove zero columns
madj(:, zero_idx_vec) = [];
madj(zero_idx_vec, :) = [];
remain_vec(zero_idx_vec) = [];
[nr, nc ] = size(madj)
madj(:,100:nr) = []
madj(100:nr,:) = []

pagerank(madj)
