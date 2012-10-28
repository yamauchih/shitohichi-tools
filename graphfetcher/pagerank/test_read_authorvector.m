function [] = test_read_authorvector()
%TEST_READ_AUTHORVECTOR test for author vector read to a cell array
%
% 
clear
% lines = read_authorvector('../vectorextractor/baseline/en_en_writer.ascii.vector');
lines = read_authorvector('../vectorextractor/baseline/en_en_writer_1.ascii.vector');
disp(lines)
