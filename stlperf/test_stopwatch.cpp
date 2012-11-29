// ==========================================================================
// StopWatch class unit test.
// ==========================================================================
/// \file
/// \brief unit test for the stop watch class
//
// New BSD License. <a href="http://en.wikipedia.org/wiki/BSD_licenses">
// http://en.wikipedia.org/wiki/BSD_licenses</a>
// Copyright (C) 2012 Hitoshi Yamauchi, Sunday Research
//

#include "StopWatch.hh"

#include <gtest/gtest.h>
#include <cmath>

/// Test StopWatch
TEST(StopWatch, StopWatch)
{
    double x = 0.0;
    stlperf::StopWatch sw;
    sw.run();
    for(int i = 0; i < 1000; i++)
    {
        for(int j = 0; j < 2000; j++)
        {
            x += sin(x) * cos(x);
        }
    }
    sw.stop();
    std::cout << "toString test: "  << sw.to_string() << std::endl;
}


int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
