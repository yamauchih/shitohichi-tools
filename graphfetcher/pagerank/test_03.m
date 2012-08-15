%TEST_03 simple sink and source node removeal test
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
[ res_madj remain_idx_vec, res_name_carray ] = ...
    remove_sink_source_node(madj, index_vec, name_carray)

% Result
%
% res_madj =
%    (2,1)        1
%    (3,2)        1
%    (1,3)        1
% 
% remain_idx_vec =
%      2
%      3
%      5
% 
% res_name_carray = 
%     'Chesher'
%     'Rabbit'
%     'Hatter'
