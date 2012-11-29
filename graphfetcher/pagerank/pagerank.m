function [ pagerank_vec ] = pagerank( M_adj )
%PAGERANK get pagerank from an adjacency matrix
%
% (C) 2012 Hitoshi Yamauchi
%

%
% get Markov matrix
%
% add up column vector
[nr, nc] = size(M_adj)
M_markov = M_adj ./ (ones(nr,1) * sum(M_adj))

% check it is Markov matrix
% sum(M_markov)

% get eigenvalues and eigen vectors
[V, Lambda] = eig(M_markov)

% get max absolute value's index of L (get the first value max index)
[m, idx] = max(diag(abs(Lambda)))

% Or find all, in case length(max(|lambda|)) > 1 (more than 1 max-s)
% d = diag(abs(Lambda))
% indices = find(max(d) == d)
maxeigen = V(:, idx)

% This vector is L2, get L1 norm
pagerank_vec = maxeigen / norm(maxeigen, 1)
