/*
 * Timer.h
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef TIMER_H_
#define TIMER_H_

// reference: https://stackoverflow.com/questions/275004/timer-function-to-provide-time-in-nano-seconds-using-c
#include <iostream>
#include <chrono>

class Timer {
private:
	typedef std::chrono::high_resolution_clock clock_;
	typedef std::chrono::duration<double, std::ratio<1> > second_;
	std::chrono::time_point<clock_> beg_;

public:
	Timer();
	virtual ~Timer();
	void reset();
	double elapsed() const;

	static std::string format_elapsed_time(double elapsed_time_sec_in_double);
	std::string format_elapsed_time();
};

#endif /* TIMER_H_ */
