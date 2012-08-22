%TEST_04_rank pagerank test, on simple three nodes.
%   

clear;
madj = sparse(7,7);
madj(2,4) = 1;
madj(2,5) = 1;
madj(3,2) = 1;
madj(4,1) = 1;
madj(5,3) = 1;
madj(6,7) = 1;
madj(7,3) = 1;


% name cell array
name_carray = {};
name_carray{1,1} = 'Alice';
name_carray{2,1} = 'Chesher';
name_carray{3,1} = 'Rabbit';
name_carray{4,1} = 'Bill';
name_carray{5,1} = 'Hatter';
name_carray{6,1} = 'Dodo';
name_carray{7,1} = 'Dormause';

index_vec = [1:7]';
[ res_madj remain_idx_vec res_name_carray ] = ...
    remove_sink_source_node(madj, index_vec, name_carray);

pagerank_vec = pagerank00(res_madj');

if(sum(pagerank_vec) < 0)
   pagerank_vec = -1 * pagerank_vec;
end

%abs_pagerank_vec = abs(pagerank_vec);
[sorted_pagerank_vec, sort_perm_idx] = sort(pagerank_vec, 'descend');

ranked_idx = index_vec(sort_perm_idx);
ranked_idx
sorted_pagerank_vec
res_name_carray(sort_perm_idx)
