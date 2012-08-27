%TEST_02 simple source node removeal test
%   

clear;
madj = sparse(5,5);
madj(1,3) = 1;
madj(2,4) = 1;
madj(3,2) = 1;
madj(4,5) = 1;
madj(5,2) = 1;

% name cell array
name_carray = {};
name_carray{1,1} = 'Alice';
name_carray{2,1} = 'Chesher';
name_carray{3,1} = 'Rabbit';
name_carray{4,1} = 'Bill';
name_carray{5,1} = 'Hatter';

index_vec = [1:5]';
[ res_madj remain_idx_vec, res_name_carray ] = ...
    remove_sink_source_node(madj, index_vec, name_carray)

% Result
%
% res_madj =
%    (3,1)        1
%    (1,2)        1
%    (2,3)        1
% 
% remain_idx_vec =
%      2
%      4
%      5
% 
% res_name_carray = 
%     'Chesher'
%     'Bill'
%     'Hatter'
