function [ removed_idx_vec ] = find_one_input_node( madj, k )
%FIND_ONE_INPUT_NODE find one input nodes
%   find size of nonzero raw is zero and size of nonzero column is one node
%   \param[in] madj adjacent matrix (not limited)
%
[nr, nc] = size(madj);
if nr ~= nc
    error('Madj is not a square matrix.')
end

[nr, nc] = size(madj);
removed_idx_vec = [];
for i = 1:nr
    % row vector is zero vector?
    if (isempty(find(madj(i,:))))
        % column nonzero size is 1
        find_col_res = size(find(madj(:,i)));
        if (find_col_res(1) == 1)
            removed_idx_vec = [removed_idx_vec i];
        end
    end
end
