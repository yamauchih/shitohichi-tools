function test_diff_ja_ja_bias_mat_0(  )
%TEST_DIFF_DIFF_JA_JA_BIAS_MAT_0 compute and visualize the ja_ja_matrix
%bias
%   

bias_mat     = ja_ja_with_navbox_writer_adj_mat();
non_bias_mat = ja_ja_writer_adj_mat();
diff_mat = bias_mat - non_bias_mat;
if (sum(sum(diff_mat < 0)))
    disp('no minus element... correct.')
end

save_fpath = 'ja_ja_with_navbox_and_without_diff'

h = figure();
hold on;

spy(diff_mat);
title('Navbox element visualization');

saveas(h, save_fpath, 'epsc');
saveas(h, save_fpath, 'png');

close(h)
disp(strcat('saving ... ', save_fpath))

end
