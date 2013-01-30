// ==========================================================================
// Elapsed time measurement.
// ==========================================================================
/// \file
/// \brief a stop watch for elapsed time measurements
//
// New BSD License. <a href="http://en.wikipedia.org/wiki/BSD_licenses">
// http://en.wikipedia.org/wiki/BSD_licenses</a>
// Copyright (C) 2012 Hitoshi Yamauchi, Sunday Research
//

#ifndef SHITOHICHI_TOOLS_STLPERF_STOPWATCH_HH
#define SHITOHICHI_TOOLS_STLPERF_STOPWATCH_HH

#include <iostream>
#include <string>
#include <sstream>
#include <sys/time.h>


namespace stlperf {

/// a stop watch for elapsed time measurements
class StopWatch
{
public:
    /// return current system time
    /// \return current system clock time
    static inline double get_current_system_time()
    {
        timeval tv;
        gettimeofday(&tv, NULL);
        double const cur_time = tv.tv_sec + (static_cast< double >(tv.tv_usec) * 1.0e-6);
        return cur_time;
    }

public:
    /// default constructor
    StopWatch()
        :
        m_is_running(false)
    {
        this->reset();
    }

    /// run the stop watch
    void run()
    {
        if(m_is_running){
            std::cerr << "Error: StopWatch::run: stop watch is running. Check your code."
                      << std::endl;
        }
        m_is_running = true;
        m_start_time = get_current_system_time();
    }

    /// stop the stop watch
    void stop()
    {
        if(!m_is_running){
            std::cerr << "Error: StopWatch::stop: stop watch is not running. Check your code."
                      << std::endl;
        }
        m_is_running = false;
        m_accumurated_time = get_current_system_time() - m_start_time;
    }

    /// reset the stop watch.
    void reset()
    {
        m_is_running       = false;
        m_start_time       = 0.0;
        m_accumurated_time = 0.0;
    }

    /// get current elapsed time.
    /// Error when the stop watch is not stop state.
    double get_elapsed_time() const
    {
        if(m_is_running){
            std::cerr << "Error: StopWatch::time: stop watch is running. "
                      << "time() call should be called only the watch is stopped. "
                      << "Check your code." << std::endl;
        }
        return m_accumurated_time;
    }

    /// get string representation with in nano, micro(us), milli, or
    /// unit seconds.
    std::string to_string() const
    {
        std::stringstream sstr;
        double const etime = get_elapsed_time();
        if(etime < 1.0e-6){
            sstr << (etime * 1.0e9) << "ns";
        }
        else if (etime < 1.0e-3){
            sstr << (etime * 1.0e6) << "us";
        }
        else if (etime < 1.0){
            sstr << (etime * 1.0e3) << "ms";
        }
        else{
            sstr << etime << "s";
        }
        return sstr.str();
    }

private:
    /// stopwatch state
    bool m_is_running;
    /// start time
    double m_start_time;
    /// accumulated time
    double m_accumurated_time;
};

/// ostream for Stopwatch
/// \param[in] os output stream
/// \param[in] sw stop watch
inline std::ostream& operator<<(std::ostream& os, StopWatch const & sw)
{
    os << sw.to_string();
    return os;
}

} // namespace stlperf
#endif // #ifndef SHITOHICHI_TOOLS_STLPERF_STOPWATCH_HH
