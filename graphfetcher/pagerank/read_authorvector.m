function [ text_content ] = read_authorvector(fname)
%READ_AUTHORVECTOR read an author vector to a cell array
%
% param[in] fname file name of author vector
% return file content string cell array
%

%
% The following UTF-8 file read doesn't work as I can see the name in the
% window, but it is possibile to keep in a binary format. However, it is
% not so useful I think.
%
% fid = fopen('ja_ja_writer.utf-8.vector', 'r', 'n', 'UTF-8');
% str = fread(fid, '*char')';
% fclose(fid);
% disp(str)
% 

% textread is obsolete.
% lines = textread(fname, '%s', 'delimiter', '\n');


fid = fopen(fname);
head_lines = textscan(fid, '#%s', 'Delimiter', '\n') ;
cells = textscan(fid, '%s', 'Delimiter', '\n') ;
fclose(fid);

lines = cells{1};

[nr, nc] = size(lines);
comment_line = [];
for i = 1:nr
    % skip comment (header)
    if lines{i, 1}(1) == '#'
        % fprintf('%s\n', lines{i,1});
        comment_line = [comment_line i];
        continue;
    else
        break;
    end
end
lines(comment_line) = [];
text_content = lines;


