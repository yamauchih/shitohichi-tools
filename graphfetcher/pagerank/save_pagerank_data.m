function save_pagerank_data(pagerank_data_mat, fname)
%SAVE_PAGERANK_DATA save the pagerank data to a file
%
% param[in] pagerank_data_mat pagerank data matrix
% param[in] fname             output file name
%

[nrows, ncols] = size(pagerank_data_mat);
if(ncols ~= 3)
  error('unexpected data of pagerank_data_mat. nx3 expected.')
end

fid = fopen(fname, 'w');

% add header
fprintf(fid, '#PageRankData 0\n');
fprintf(fid, '# PageRank computation data result\n');
fprintf(fid, '# Copyright (C) 2012 Hitoshi Yamauchi\n');
fprintf(fid, '#\n');
fprintf(fid, '# result_index pagerank sorted_permulation_index\n');
fprintf(fid, '#\n');

% output the data
fprintf(fid, '%d %g %d\n', pagerank_data_mat');

fclose(fid);


