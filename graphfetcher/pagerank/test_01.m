%TEST_01 simple sink node removeal test
%   
% madj = [0, 1, 0, 1, 0;
%         0, 0, 1, 0, 0;
%         1, 0, 0, 0, 0;
%         0, 0, 0, 0, 0;
%         0, 0, 0, 1, 0;
%        ];

clear;
madj = sparse(5,5);
madj(1,2) = 1;
madj(1,4) = 1;
madj(2,3) = 1;
madj(3,1) = 1;
%madj(5,4) = 1;
madj(4,5) = 1;

% name cell array
name_carray = {}
name_carray{1,1} = 'Alice';
name_carray{2,1} = 'Chesher';
name_carray{3,1} = 'Rabbit';
name_carray{4,1} = 'Bill';
name_carray{5,1} = 'Hatter';

index_vec = [1:5]';
[ res_madj remain_idx_vec res_name_carray ] = ...
    remove_sink_source_node(madj, index_vec, name_carray)

% Result
%
% res_madj =
%      0     1     0
%      0     0     1
%      1     0     0
% remain_idx_vec =
%      1
%      2
%      3
% res_name_carray = 
%     'Alice'
%     'Chesher'
%     'Rabbit'    
%      
