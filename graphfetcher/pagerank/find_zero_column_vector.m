function [ removed_idx_vec ] = find_zero_column_vector( madj )
%FIND_ZERO_COLUMNVECTOR find zero column vectors
%   find zero column vectors and return the indeces
%   
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[nr, nc] = size(madj);
removed_idx_vec = [];
% find zero vectors
for i = 1:nc
    % for sparse matrix find(X,k) is not possible
    if (isempty(find(madj(:,i))))
        removed_idx_vec = [removed_idx_vec i];
    end
end
