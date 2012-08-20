%TEST_EN_EN_PAGERANK Summary of this function goes here
%   Detailed explanation goes here

madj = en_en_writer_adj_mat_selected();
author_vec = read_authorvector('en_en_writer.ascii.vector');

% create the initial index vector
[nr, nc] = size(madj);
if (nr ~=nc)
    error('madj is not a squere matrix.')
end

[ar ac] = size(author_vec);
if (nr ~= ar)
    error('author vector size does not agree with madj.')
end
index_vec = [1:nr]';

% remove source nodes and sink nodes
[ res_madj res_idx_vec, res_author_vec ] = ...
    remove_sink_source_node(madj, index_vec, author_vec);

%pagerank_vec = pagerank00(res_madj');
pagerank_vec = pagerank00(res_madj');

if(sum(pagerank_vec) < 0)
   pagerank_vec = -1 * pagerank_vec;
end

%abs_pagerank_vec = abs(pagerank_vec);
[sorted_pagerank_vec, sort_perm_idx] = sort(pagerank_vec, 'descend');

ranked_idx = index_vec(sort_perm_idx);
ranked_idx(1:10)
sorted_pagerank_vec(1:10)
