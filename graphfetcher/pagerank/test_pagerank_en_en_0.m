%TEST_PAGERANK_EN_EN_0 pagerank computation for en_en
%

clear

% data
vector_fname = '/../vectorextractor/baseline/en_en_writer.ascii.vector';
res_fname    = 'pagerank_result/en_en_writer.pagerank_res.vector'; 

% author vector
current_dir = pwd();
author_vec_fpath = strcat(current_dir, vector_fname);
author_vec = read_authorvector(author_vec_fpath);

% adjacent matrix
%
% if adjacent matrix cannot be found, add the path.
% adj_mat_data_dir = '/../graphextractor/baseline/';
% addpath(strcat(current_dir, adj_mat_data_dir));
%
madj = en_en_writer_adj_mat();

% create the initial index vector
[nr, nc] = size(madj);
if (nr ~=nc)
    error('madj is not a squere matrix.')
end

[ar, ac] = size(author_vec);
if (nr ~= ar)
    error('author vector size does not agree with madj.')
end
index_vec = [1:nr]';

% remove source nodes and sink nodes
[ res_madj, res_idx_vec, res_name_carray ] = ...
    remove_sink_source_node(madj, index_vec, author_vec);

%pagerank_vec = pagerank00(res_madj');
pagerank_vec = pagerank01(res_madj');

if(sum(pagerank_vec) < 0)
   pagerank_vec = -1 * pagerank_vec;
end

%abs_pagerank_vec = abs(pagerank_vec);
[sorted_pagerank_vec, sort_perm_idx] = sort(pagerank_vec, 'descend');

ranked_idx = index_vec(sort_perm_idx);
%ranked_idx(1:100)
%sorted_pagerank_vec(1:100)
%res_name_carray(sort_perm_idx(1:50));

save_authorvector(res_name_carray(sort_perm_idx), res_fname);
