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
iter = 0;
while (~isempty(find(sum(madj') == 0)))
    [ res_madj remain_idx_vec ] = remove_sink_source_node(madj, index_vec);
    madj = res_madj;
    index_vec = remain_idx_vec;
    iter = iter + 1;
    [nr, nc] = size(madj);
    fprintf('%d iters. size(%d,%d)\n', iter, nr, nc);
end

%pagerank_vec = pagerank00(res_madj');
pagerank_vec = pagerank01(res_madj');

if(sum(pagerank_vec) < 0)
   pagerank_vec = -1 * pagerank_vec;
end

%abs_pagerank_vec = abs(pagerank_vec);
[sorted_pagerank_vec, sort_perm_idx] = sort(pagerank_vec, 'descend');

ranked_idx = index_vec(sort_perm_idx);
ranked_idx(1:10)
sorted_pagerank_vec(1:10)
