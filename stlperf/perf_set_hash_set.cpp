// ==========================================================================
// Performance of set and hash_set comparison.
// ==========================================================================
/// \file
/// \brief a simple performance test for STL set and hash_set
//
// New BSD License. <a href="http://en.wikipedia.org/wiki/BSD_licenses">
// http://en.wikipedia.org/wiki/BSD_licenses</a>
// Copyright (C) 2012 Hitoshi Yamauchi, Sunday Research
//

#include <set>
#include <ext/hash_set>
#include <stdlib.h>

#include "StopWatch.hh"

// performance comparison of set and hash_set
int main(int argc, char *argv[])
{
    const int RepeatCount  = 1;
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
// set.insert():      4.58868s
// hash_set.insert(): 905.446ms
// set.find():        2.47205s
// hash_set.find():   344.448ms
// set.erase():       2.1649s
// hash_set.erase():  284.121ms
//

// <table border="1">
//  <tr>
//   <td>Method</td>
//   <td>set</td>
//   <td>hash_set</td>
//  </tr>
//  <tr>
//   <td>insert()</td>
//   <td>7.31 sec</td>
//   <td>922  millisec</td>
//  </tr>
//  <tr>
//   <td>find()</td>
//   <td>4.95 sec</td>
//   <td>255  millisec</td>
//  </tr>
//  <tr>
//   <td>erase()</td>
//   <td>2.12 sec</td>
//   <td>301  millisec</td>
//  </tr>
// </table>
