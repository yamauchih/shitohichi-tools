function [ text_content ] = read_authorvector(fname)
%TEST_OPEN_AUTHORVECTOR test for author vector read to a cell array
%
% \param[in] fname file name of author vector
% \return file content string cell array
%
%
% The following UTF-8 file read doesn't workaas I can see the name in the
% window, but it is possibile to keep in a binary format. However, it is
% not so useful I think.
%
% fid = fopen('ja_ja_writer.vector', 'r', 'n', 'UTF-8');
% str = fread(fid, '*char')';
% fclose(fid);
% disp(str)
% 

lines = textread(fname, '%s', 'delimiter','\n');
[nr nc] = size(lines);
headerline = [];
for i = 1:nr
    % skip comment (header)
    if lines{i, 1}(1) == '#'
        % fprintf('%s\n', lines{i,1});
        headerline = [headerline i];
        continue;
    else
        break;
    end
end
lines(headerline) = [];
text_content = lines;
