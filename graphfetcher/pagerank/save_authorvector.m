function save_authorvector(author_vec, fname)
%SAVE_AUTHORVECTOR save the author vector to a file
%
% param[in] author_vec author string cell array vector.
% param[in] fname      output file name
%

[nrows, ncols] = size(author_vec);
fid = fopen(fname, 'w');

fprintf(fid, '# pagerank computation result\n');
fprintf(fid, '# Hitoshi Yamauchi 2012\n');
for i = 1:nrows
  fprintf(fid, '%s\n', author_vec{i,1});
end

fclose(fid);


