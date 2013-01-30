function test_show_adjacency_mat_0(  )
%TEST_SHOW_ADJACENT_MAT_0 show adjacency matrix
%   

% function handle vector is not supported in matlab 2006a
madj_list = {
    @de_en_writer_adj_mat
    @de_de_writer_adj_mat
    @de_ja_writer_adj_mat

    @en_en_writer_adj_mat
    @en_de_writer_adj_mat
    @en_ja_writer_adj_mat

    @ja_en_writer_adj_mat
    @ja_de_writer_adj_mat
    @ja_ja_writer_adj_mat
    @ja_ja_writer_adj_mat_with_navbox

    @italian_en_writer_adj_mat
    @italian_en_no_navbox_writer_adj_mat
};
title_list = {
    'German author adjacency matrix in en.wikipedia.org'
    'German author adjacency matrix in de.wikipedia.org'
    'German author adjacency matrix in ja.wikipedia.org'

    'English author adjacency matrix in en.wikipedia.org'
    'English author adjacency matrix in de.wikipedia.org'
    'English author adjacency matrix in ja.wikipedia.org'

    'Japanese author adjacency matrix in en.wikipedia.org'
    'Japanese author adjacency matrix in de.wikipedia.org'
    'Japanese author adjacency matrix (no navbox) in ja.wikipedia.org'
    'Japanese author adjacency matrix in ja.wikipedia.org'

    'Italian author adjacency matrix in en.wikipedia.org'
    'Italian author adjacency matrix (no navbox) in en.wikipedia.org'
    };
save_fbase_list = {
    'de_en_madj'
    'de_de_madj'
    'de_ja_madj'

    'en_en_madj'
    'en_de_madj'
    'en_ja_madj'

    'ja_en_madj'
    'ja_de_madj'
    'ja_ja_madj'
    'ja_ja_madj_with_navbox'

    'italian_en_madj_with_navbox'
    'italian_en_madj_no_navbox'
    };
     
% for i = 1:length(madj_list)
for i = 12:12
    save_one_figure(madj_list{i}, title_list{i}, save_fbase_list{i});
end

end
%% one figure save function
function save_one_figure(mat_gen_func_handle, fig_title, save_fpath)
    
h = figure();
hold on;

spy(mat_gen_func_handle());
title(fig_title);

saveas(h, save_fpath, 'epsc');
saveas(h, save_fpath, 'png');

close(h)
disp(strcat('saving ... ', save_fpath))
end
