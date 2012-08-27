function [ pagerank_vec ] = pagerank01( M_adj )
%PAGERANK01 get pagerank from an adjacency matrix with random choise
% (C) 2012 Hitoshi Yamauchi
%

% This should be empty
zero_idx_vec = find(sum(M_adj) == 0);
if (~isempty(zero_idx_vec))
    error('zero index column vector found.');
end

pagerank_factor = 0.15;

%
% get Markov matrix
%
% add up column vector
M_adj = full(M_adj);
[nr, nc] = size(M_adj);
M_adj = M_adj + ((pagerank_factor / nr) * ones(nr, nc));
M_markov = M_adj ./ (ones(nr,1) * sum(M_adj));

% check it is Markov matrix
% sum(M_markov)

% check the rank
rank_m = rank(full(M_markov));
if (rank_m < nr)
    fprintf(1, 'warn: M_adj is not full rank (%d of %d)\n', rank_m, nr);
end

% get eigenvalues and eigen vectors
[V, Lambda] = eig(M_markov);

% get max absolute value's index of L (get the first value max index)
% [m, idx] = max(diag(abs(Lambda)));
[m, idx] = max(abs(real(diag(Lambda))));
fprintf(1, 'max eigenvalue = %g+%gi\n', real(m), imag(m));

% Or find all, in case length(max(|lambda|)) > 1 (more than 1 max-s)
% d = diag(abs(Lambda))
% indices = find(max(d) == d)
maxeigen = V(:, idx);

% This vector is L2, get L1 norm
pagerank_vec = maxeigen / norm(maxeigen, 1);
