function [] = test_save_authorvector()
%TEST_SAVE_AUTHORVECTOR test saving an author vector to a file
%
% 

author_vec_cell{1,1} = 'Murakami_Haruki';
author_vec_cell{2,1} = 'Natume_Souseki';
author_vec_cell{3,1} = 'Rebecca_M';

fname = 'test_res.vector';
save_authorvector(author_vec_cell, fname);

