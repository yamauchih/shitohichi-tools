// ==========================================================================
// performance of map copy
// ==========================================================================
// Copyright (C) 2012 Hitoshi Yamauchi
// ==========================================================================
/// \file
/// \brief a simple performance test for STL nth_element

//
// (print (random) (current-buffer))
//
#include <algorithm>
#include <iostream>
#include <iterator>
#include <stdlib.h>
#include <vector>

#include "StopWatch.hh"

/// get median by sort
int get_median_by_sort(std::vector< int > & comp_buf)
{
    size_t median_idx = comp_buf.size() / 2;
    std::sort(comp_buf.begin(), comp_buf.end());
    return comp_buf[median_idx];
}

/// get median by nth_element
int get_median_by_nth_element(std::vector< int > & comp_buf)
{
    size_t median_idx = comp_buf.size() / 2;
    std::nth_element(comp_buf.begin(), comp_buf.begin() + median_idx, comp_buf.end());
    return comp_buf[median_idx];
}

/// performance test of nth element
/// \param[in] array_size      size of the array of median computation
/// \param[in] iteration_count iteration count
void perf_nth_element(int array_size,  int iteration_count)
{
    //
    // get 4096 elements from a pseudo-random number array. The 4096
    // elements widow will be shifted one by one.  Then the median of
    // this 4096 elements are computed by sort or nth_element.
    //
    std::cout << "array_size: " << array_size
              << ", iteration_count: " << iteration_count << std::endl;

    std::vector< int > rand_vec(iteration_count + array_size);
    srand48(0);                 // for reproduction, set the same seed

    for(int i = 0; i < (iteration_count + array_size); ++i){
        rand_vec.push_back(lrand48());
    }
    size_t const median_idx = array_size / 2;

    std::vector< int > res_by_sort(iteration_count);
    std::vector< int > res_by_nth(iteration_count);
    std::vector< int > comp_buf(array_size);

    stlperf::StopWatch sw0;
    sw0.run();
    // get medians by sort
    for(int i = 0; i < iteration_count; ++i){
        comp_buf.clear();
        for(int j = 0; j < array_size; ++j){
            comp_buf.push_back(rand_vec[i+j]);
        }

        res_by_sort.push_back(get_median_by_sort(comp_buf));
    }
    sw0.stop();
    std::cout << "get medians by sort: " << sw0 << std::endl;

    stlperf::StopWatch sw1;
    sw1.run();
    // get medians by nth_element
    for(int i = 0; i < iteration_count; ++i){
        comp_buf.clear();
        for(int j = 0; j < array_size; ++j){
            comp_buf.push_back(rand_vec[i+j]);
        }

        res_by_nth.push_back(get_median_by_nth_element(comp_buf));
    }
    sw1.stop();
    std::cout << "get medians by nth element: " << sw1 << std::endl;

    // compare the result
    bool is_ok = true;
    for(int i = 0; i < iteration_count; ++i){
        if(res_by_nth[i] != res_by_sort[i]){
            is_ok = false;
            break;
        }
    }

    std::cout << "result validation ... ";
    if(is_ok){
        std::cout << "passed.";
    }
    else{
        std::cout << "failed.";
    }
    std::cout << std::endl;
}

/// main
int main()
{
    int const iteration_count = 100000;
    int array_size[] = {
        4096, 8192, 16384, 32768, 65536, -1,
    };

    for(int i = 0; array_size[i] > 0; ++i){
        perf_nth_element(array_size[i], iteration_count);
    }

    return 0;
}

//
// Result:
// CPU: Intel(R) Core(TM) i7-2720QM CPU @ 2.20GHz
// OS:  3.2.0-29-generic #46-Ubuntu SMP Fri Jul 27 17:03:23 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux
//
// iteration_count: 100000
//             by sort       by nth_element
// Array size
// 4096         4.20396s     1.18444s
// 8192         8.98214s     2.30188s
// 16384       19.2758 s     4.58939s
// 32768       40.9374 s     9.3263 s
// 65536       88.0514 s    18.7449 s
//
