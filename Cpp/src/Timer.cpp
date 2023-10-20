/*
 * Timer.cpp
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#include "Timer.h"
#include "YyxUtils.h"

Timer::Timer() : beg_(clock_::now()) {
}

Timer::~Timer() {
}

void Timer::reset(){
	beg_ = clock_::now();
}
double Timer::elapsed() const {
	return std::chrono::duration_cast<second_>(clock_::now() - beg_).count();
}

std::string Timer::format_elapsed_time(double elapsed_time_sec_in_double){
//	int elapsed_time = end_time - start_time;
	int elapsed_time = (int) elapsed_time_sec_in_double;
	int day = elapsed_time / (3600*24);
	int hour = elapsed_time % (3600*24) / 3600;
	int min = elapsed_time % 3600 / 60;
	double sec = elapsed_time_sec_in_double - elapsed_time / 60 * 60;

	std::string ans = "";
//	printf("[Elapsed-Time] ");
	if(day > 0){
		ans += string_format("%dday ", day);
	}
	if(hour > 0){
		ans += string_format("%dh", hour);
	}
	if(min > 0){
		ans += string_format("%dmin", min);
	}
	if(sec > 0 || ans == ""){
		ans += string_format("%.7fs", sec);
	}
	return ans;
}

std::string Timer::format_elapsed_time(){
	return format_elapsed_time(elapsed());
}
