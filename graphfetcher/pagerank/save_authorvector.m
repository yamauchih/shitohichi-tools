function save_authorvector(author_vec, fname)
%SAVE_AUTHORVECTOR save the author vector to a file
%
% param[in] author_vec author string cell array vector.
% param[in] fname      output file name
%

[nrows, ncols] = size(author_vec);
fid = fopen(fname, 'w');

% add header
fprintf(fid, '#PageRankAuthor 0\n');
fprintf(fid, '# Author vector result sorted by pagerank\n');
fprintf(fid, '# Copyright (C) 2012 Hitoshi Yamauchi\n');
fprintf(fid, '#\n');

% output the data
for i = 1:nrows
  fprintf(fid, '%s\n', author_vec{i,1});
end

fclose(fid);


