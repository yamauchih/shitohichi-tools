// ==========================================================================
// performance of map copy
// ==========================================================================
// Copyright (C) 2012 Hitoshi Yamauchi
// ==========================================================================

#include <map>
#include <string>
#include <stdlib.h>

#include "StopWatch.hh"

/// create map (copy source) with 50 entries
std::map< std::string, int > create_map_00()
{
    char const * const p_key[] = {
        "nb_subcubes",
        "nb_subcubes_rendered",
        "size_volume_data_rendered",
        "size_horizon_data_rendered",
        "nb_horizon_triangles_rendered",
        "time_rendering_horizon",
        "time_rendering_volume",
        "time_rendering_volume_and_horizon",
        "time_intersection_lines_points",
        "time_rendering_only",
        "time_generic_1",
        "time_generic_2",
        "time_generic_3",
        "value_generic_1",
        "value_generic_2",
        "value_generic_3",
        "time_gpu_upload",
        "time_gpu_download",
        "time_rendering",
        "time_rendering_total_sum",
        "size_volume_data_upload",
        "size_rendering_results_download",
        "size_pinned_host_memory",
        "size_unpinned_host_memory",
        "size_gpu_memory",
        "nb_fragments",
        "is_using_gpu",
        "time_total_rendering",
        "time_total_compositing",
        "time_total_final_compositing",
        "time_complete_frame",
        "time_frame_setup",
        "time_frame_finish",
        "time_avg_rendering",
        "frames_per_second",
        "nb_active_hosts",
        "nb_horizontal_spans",
        "nb_rendering_results_in_queue",
        "nb_sub_clusters",
        "size_span_transfer",
        "size_span_transfer_compressed",
        "size_intermediate_image_transfer",
        "size_intermediate_image_composited",
        "time_compositing_stage",
        "time_image_compositing",
        "time_image_transfer",
        "nb_composited_leafs",
        "nb_considered_leafs_per_span",
        0,
    };

    std::map< std::string, int > amap;
    for(int i = 0; p_key[i] != 0; ++i){
        amap[p_key[i]] = i;
    }
    return amap;
}

/// create map (copy source) with 50 entries
std::map< std::string, int > create_map_01()
{
    // 100 entries of English writer
    char const * const p_key[] = {
        "Edwin_Abbott_Abbott",
        "Gilbert_Abbott_Beckett",
        "George_Abbot",
        "Kia_Abdullah",
        "Lascelles_Abercrombie",
        "Paul_Ableman",
        "J._R._Ackerley",
        "Rodney_Ackland",
        "Peter_Ackroyd",
        "Eliza_Acton",
        "Harold_Acton",
        "Douglas_Adams",
        "Richard_Adams",
        "Sarah_Fuller_Flower_Adams",
        "Donald_Adamson",
        "Arthur_St._John_Adcock",
        "Fleur_Adcock",
        "Joseph_Addison",
        "Percy_Addleshaw",
        "Diran_Adebayo",
        "Mark_Adlard",
        "James_Agate",
        "John_Aglionby",
        "Grace_Aguilar",
        "Janet_and_Allan_Ahlberg",
        "Robert_Aickman",
        "Joan_Aiken",
        "Arthur_Aikin",
        "Lucy_Aikin",
        "John_Aikin",
        "Alfred_Ainger",
        "William_Harrison_Ainsworth",
        "Mark_Akenside",
        "William_Alabaster",
        "James_Albery",
        "Alice_Albinia",
        "Mary_Alcock",
        "Thomas_Aldham",
        "Richard_Aldington",
        "Brian_Aldiss",
        "Henry_Aldrich",
        "Monica_Ali",
        "Cyril_Alington",
        "Nicholas_Allan",
        "James_Allen_(author)",
        "Walter_Allen",
        "Margery_Allingham",
        "Drummond_Allison",
        "Kenneth_Allott",
        "Kenneth_Allsop",
        "E._M._Almedingen",
        "John_Almon",
        "David_Almond",
        "Vincent_Alsop",
        "Al_Alvarez",
        "Moniza_Alvi",
        "Eric_Ambler",
        "Isaac_Ambrose",
        "Elizabeth_Frances_Amherst_(poet)",
        "Kingsley_Amis",
        "Martin_Amis",
        "Thomas_Amory_(author)",
        "Thomas_Amory_(tutor)",
        "Valerie_Anand",
        "Patrick_Anderson_(poet)",
        "Lancelot_Andrewes",
        "Roger_Andrewes",
        "Miles_Peter_Andrews",
        "Norman_Angell",
        "Jane_Anger",
        "Peter_Anghelides",
        "George_Anson,_1st_Baron_Anson",
        "Christopher_Anstey",
        "Charles_James_Apperley",
        "Lisa_Appignanesi",
        "Roy_Apps",
        "Arthur_John_Arberry",
        "Harriet_Arbuthnot",
        "John_Arbuthnot",
        "Fred_Archer_(writer)",
        "Jeffrey_Archer",
        "Philip_Ardagh",
        "John_Arden",
        "Edward_Ardizzone",
        "Reginald_Arkell",
        "Michael_Arlen",
        "John_Arlott",
        "Robert_Armin",
        "Simon_Armitage",
        "Martin_Armstrong_(writer)",
        "Peter_Armstrong_(poet)",
        "Richard_Armstrong_(author)",
        "Elizabeth_von_Arnim",
        "Edwin_Arnold",
        "Edwin_Lester_Linden_Arnold",
        "Elizabeth_Arnold_(children's_writer)",
        "Matthew_Arnold",
        "Richard_Arnold_(chronicler)",
        "Thomas_Arnold",
        "Thomas_Walker_Arnold",
        0,
    };
    std::map< std::string, int > amap;
    for(int i = 0; p_key[i] != 0; ++i){
        amap[p_key[i]] = i;
    }
    return amap;
}

//
//  50 entries 1.44/100000 = 14.4 microsecond
// 100 entries 3.30/100000 = 33   microsecond
//
int main(int argc, char *argv[])
{
    const int RepeatCount  = 100000;

    // map copy test
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int j = 0; j < RepeatCount; ++j){
            // std::map< std::string, int > src = create_map_00();
            std::map< std::string, int > src = create_map_01();
            std::map< std::string, int > copied_map = src;
        }
        sw.stop();
        double milisec = 1.0e3 * sw.get_elapsed_time() / static_cast< double >(RepeatCount);
        std::cout << "map copy: " << sw << ", " << milisec << " millisec/iter" << std::endl;
    }
}
