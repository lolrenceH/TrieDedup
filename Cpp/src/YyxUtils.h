/*
 * ACGTNMap.h
 *
 *  Created on: Jan 28, 2023
 *      Author: Adam Yongxin Ye @ BCH
 */

#ifndef YYXUTILS_H_
#define YYXUTILS_H_

#include <memory>
#include <stdexcept>
#include <cstdio>
//#include <iostream>

// reference: https://stackoverflow.com/questions/7433448/eclipse-cdt-symbol-null-could-not-be-resolved
#ifndef NULL
#define NULL  ((void *) 0)
#endif

// reference: https://stackoverflow.com/questions/2342162/stdstring-formatting-like-sprintf
template<typename ... Args>
std::string string_format( const std::string& format, Args ... args )
{
//	int size_s = std::snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for '\0'
	char buf1[1000];
	int size_s = std::snprintf( buf1, 1000, format.c_str(), args ... ) + 1; // Extra space for '\0'
	if( size_s <= 0 ){ throw std::runtime_error( "Error during formatting." ); }
	auto size = static_cast<size_t>( size_s );
	std::unique_ptr<char[]> buf( new char[ size ] );
	std::snprintf( buf.get(), size, format.c_str(), args ... );
//	return std::string( buf.get(), buf.get() + size - 1 ); // We don't want the '\0' inside
	return std::string(buf.get());
}

#endif /* YYXUTILS_H_ */
