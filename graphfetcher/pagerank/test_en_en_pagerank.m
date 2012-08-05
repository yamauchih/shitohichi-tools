%TEST_EN_EN_PAGERANK Summary of this function goes here
%   Detailed explanation goes here

madj = en_en_writer_adj_mat_selected();

% create the initial index vector
[nr, nc] = size(madj);
if (nr ~=nc)
    error('madj is not a squere matrix.')
end
index_vec = [1:nr]';

%
% check the row vector has no zero vector. Row vector since Markov matrix
% will be transposed (transposed column vector is checked.)
%
iter = 0
while (~isempty(find(sum(madj') == 0)))
    [ res_madj remain_idx_vec ] = remove_sink_source_node(madj, index_vec);
    madj = res_madj;
    index_vec = remain_idx_vec;
    iter = iter + 1;
    [nr, nc] = size(madj);
    fprintf('%d iters. size(%d,%d)\n', iter, nr, nc);
end

pagerank_vec = pagerank(res_madj');
abs_pagerank_vec = abs(pagerank_vec);
idx_idx = find(abs_pagerank_vec == max(abs_pagerank_vec))
index_vec(idx_idx)
