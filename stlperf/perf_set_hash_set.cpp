// ==========================================================================
// performance of map copy
// ==========================================================================
// Copyright (C) 2012 Hitoshi Yamauchi
// ==========================================================================
/// \file
/// \brief a simple performance test for STL set and hash_set

#include <set>
#include <ext/hash_set>
#include <stdlib.h>

#include "StopWatch.hh"

// performance comparison of set and hash_set
int main(int argc, char *argv[])
{
    const int RepeatCount  = 2;
    const int ElementCount = 10000000;

    std::set< int >      test_set;
    __gnu_cxx::hash_set< int > test_hash_set;

    // random number is better, but then if random number generation is
    // a heavy task? I cannot measure the set and hash_set performance.

    // insertion test
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int j = 0; j < RepeatCount; ++j){
            for(int i = 0; i < ElementCount; ++i){
                test_set.insert(i);
            }
        }
        sw.stop();
        std::cout << "set.insert():      " << sw << std::endl;
    }

    {
        stlperf::StopWatch sw;
        sw.run();
        for(int j = 0; j < RepeatCount; ++j){
            for(int i = 0; i < ElementCount; ++i){
                test_hash_set.insert(i);
            }
        }
        sw.stop();
        std::cout << "hash_set.insert(): " << sw << std::endl;
    }

    // search test
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int j = 0; j < RepeatCount; ++j){
            for(int i = 0; i < ElementCount; ++i){
                if(test_set.find(i) == test_set.end()){
                    std::cout << "Should not be here!, must find." << std::endl;
                }
            }
        }
        sw.stop();
        std::cout << "set.find():        " << sw << std::endl;
    }
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int j = 0; j < RepeatCount; ++j){
            for(int i = 0; i < ElementCount; ++i){
                if(test_hash_set.find(i) == test_hash_set.end()){
                    std::cout << "Should not be here!, must find." << std::endl;
                }
            }
        }
        sw.stop();
        std::cout << "hash_set.find():   " << sw << std::endl;
    }

    // remove test
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int i = 0; i < ElementCount; ++i){
            test_set.erase(i);
        }
        sw.stop();
        std::cout << "set.erase():       " << sw << std::endl;
    }
    {
        stlperf::StopWatch sw;
        sw.run();
        for(int i = 0; i < ElementCount; ++i){
            test_hash_set.erase(i);
        }
        sw.stop();
        std::cout << "hash_set.erase():  " << sw << std::endl;
    }
}


//
// Result:
// CPU: Intel(R) Core(TM) i7-2720QM CPU @ 2.20GHz
// OS:  3.2.0-29-generic #46-Ubuntu SMP Fri Jul 27 17:03:23 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux
//
// Simple test.
//
// A continuous number sequence is inserted. The result is heavily
// depends on the input sequence of hash_set because of the hash
// function's property. Please do not use this result if you don't
// know what this means. This is just one sample. (However, I prefer
// set since usually set is more stable to the input sequence. This is
// just my preference. Any hash functions you can fool if you know
// it.)
//
// set.insert():      7.30689s
// hash_set.insert(): 921.765ms
// set.find():        4.95401s
// hash_set.find():   254.803ms
// set.erase():       2.11941s
// hash_set.erase():  300.573ms
//
