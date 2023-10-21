#!/usr/bin/env python3


import sys, os, os.path, subprocess, time


### flushing print, reference: https://mail.python.org/pipermail/python-list/2015-November/698426.html
def _print(*args, **kwargs):
	file = kwargs.get('file', sys.stdout)
	print(*args, **kwargs)
	file.flush()

def die(message):
	sys.stderr.write(message + "\n")
	sys.exit(1)


### reference: Yyx_system_command_functions.20160607.pl, tlx2bed_v3.py

def check_elapsed_time(start_time):
	end_time = time.time()
	elapsed_time = end_time - start_time
	day = int(elapsed_time / (3600*24))
	hour = int(elapsed_time % (3600*24) / 3600)
	min = int(elapsed_time % 3600 / 60)
	sec = elapsed_time % 60
	elapsed_time = ''
	if day>0 : elapsed_time += '{}day '.format(day)
	if hour>0: elapsed_time += '{}h'.format(hour)
	if min>0 : elapsed_time += '{}min'.format(min)
	if sec>0 or elapsed_time == '': elapsed_time += '{:.2f}s'.format(sec)
	_print('[PYTHON-TIME] ' + elapsed_time, file=sys.stderr)


def check_is_empty_dir(dirname):
	if os.path.isdir(dirname):
		for nowDirName, subdirList, fileList in os.walk(dirname):
			if nowDirName == '.':
				return len(subfileList) == 0
			else:
				continue
	else:
		_print('Warning: Not a dir is attemped to be checked', file=sys.stderr)
		return None
		

def exist_file_or_dir(filenames, prompt_str, mode='any'):
	if mode not in ('any', 'all'):
		_print('Error: mode should be either "any" or "all", in exist_file_or_dir()', file=sys.stderr)
		return None
	is_mode_all = False
	if mode == 'any':
		is_mode_all = True
		
	if isinstance(filenames, str):
		filenames = [filenames]
	not_None_count = 0
	for filename in filenames:
		if filename is None:
			continue
		not_None_count += 1
		if os.path.isdir(filename):
			if not check_is_empty_dir(filename):
				_print('[CHECK-EXIST] Dir ' + filename + ' has already existed, and not empty. ' + prompt_str, file=sys.stderr)
				if not is_mode_all:
					return True
			else:
				if is_mode_all:
					return False
		elif os.path.isfile(filename) and os.path.getsize(filename) >= 100:
			# os.path.getsize(x) may also be os.stat(x).st_size
			_print('[CHECK-EXIST] File ' + filename + ' has already existed. ' + prompt_str, file=sys.stderr)
			if not is_mode_all:
				return True
		else:
			if is_mode_all:
				return False
	if not_None_count > 0:
		return is_mode_all
	return False
	

def check_final_file_then_remove_intermediate_file(final_filenames, intermediate_filenames, mode='all'):
	if mode not in ('any', 'all'):
		_print('Error: mode should be either "any" or "all", in check_final_file_then_remove_intermediate_file()', file=sys.stderr)
		return
		
	if isinstance(intermediate_filenames, str):
		intermediate_filenames = [intermediate_filenames]
	if exist_file_or_dir(final_filenames, 'So remove intermediate files...', mode=mode):
		for filename in intermediate_filenames:
			if filename is None:
				continue
			if os.path.exists(filename):
				_print('[PYTHON-REMOVE] ' + filename, file=sys.stderr)
				os.remove(filename)

def check_file_then_exec_command(filenames, command, should_time=False, error_stop=False, not_run=False):
	start_time = time.time()
	
	_print('[SUBPROCESS-CALL] ' + command, file=sys.stderr)
	if exist_file_or_dir(filenames, 'Skip this above command...', mode='any'):
		return
	
	if not not_run:
#		returnValue = os.system('/bin/bash -c ' + command)
		returnValue = subprocess.call(['/bin/bash', '-c', command])
		if returnValue != 0:
			if error_stop:
				_print('Error: when exec last command, return value = {}'.format(returnValue), file=sys.stderr)
				sys.exit(returnValue)
	
	if should_time:
		check_elapsed_time(start_time)


def stop_if_file_not_exist(filenames, mode='any'):
	if mode not in ('any', 'all'):
		_print('Error: mode should be either "any" or "all", in stop_if_file_not_exist()', file=sys.stderr)
		return None
	is_mode_all = False
	if mode == 'any':
		is_mode_all = True
		
	if isinstance(filenames, str):
		filenames = [filenames]
	checkFileNumber = 0
	missingFileNumber = 0
	for filename in filenames:
		if filename is None:
			continue
		checkFileNumber += 1
		if not os.path.isfile(filename):
			# os.path.getsize(x) may also be os.stat(x).st_size
			_print('[CHECK-EXIST] File ' + filename + ' does not exist.', file=sys.stderr)
			missingFileNumber += 1
		else:
			_print('[CHECK-EXIST] File ' + filename + ' exists.  Good.', file=sys.stderr)
	if missingFileNumber > 0:
		if not is_mode_all:
			_print('[STOP-NOT-EXIST] Error: requested {} file(s) is missing. Terminate!'.format(missingFileNumber), file=sys.stderr)
			sys.exit(missingFileNumber)
		elif missingFileNumber == checkFileNumber:
			_print('[STOP-NOT-EXIST] Error: requested file(s) is missing. Terminate!', file=sys.stderr)
			sys.exit(missingFileNumber)


def str2bool(x):
	try:
		x = int(x)
		return x > 0
	except ValueError:
		return x.lower() in ('true', 't', 'yes', 'y')



usage = '''
Usage: python this.py <implementation> <subcommand> <input>
	[output] [max_missing] [sorted]

<implementation>\t one of 'cpp', 'java' or 'python'
<subcommand>    \t one of 'sortuniq', 'trie' or 'pairwise'
<input>         \t input *.fasta, *.fa, *.fastq or *.fq file
[output]        \t output *.fasta or *.fa (optional; default: empty = STDOUT)
[max_missing]   \t max allowed ambiguous Ns per read (optional; default: 9999)
[sorted]        \t is the input file has already been sorted by the number of Ns (optional; default: False)
'''

if len(sys.argv) < 4:
	die('Error: not enough arguments' + usage)

implementation = sys.argv[1]
subcommand = sys.argv[2]
input_filename = sys.argv[3]

if implementation.lower() != 'cpp' and implementation.lower() != 'java' and implementation.lower() != 'python':
	die('Error: unrecognized implementation "{implementation}"' + ", which should be one of 'cpp', 'java' or 'python'" + usage)

if subcommand.lower() != 'sortuniq' and subcommand.lower() != 'trie' and subcommand.lower() != 'pairwise':
	die('Error: unrecognized subcommand "{subcommand}"' + ", which should be one of 'sortuniq', 'trie' or 'pairwise'" + usage)

if implementation.lower() == 'python' and subcommand.lower() == 'sortuniq':
	die('Error: python implementation does not support subcommand sortuniq.  Please switch to cpp or java implementation instead.' + usage)

arg_idx = 4
output_filename = ''
if len(sys.argv) > arg_idx:
	output_filename = sys.argv[arg_idx]

arg_idx += 1
max_missing = 9999
if len(sys.argv) > arg_idx:
	max_missing = float(sys.argv[arg_idx])

arg_idx += 1
is_input_sorted = False
if len(sys.argv) > arg_idx:
	is_input_sorted = str2bool(sys.argv[arg_idx])

_print(f'[CMD-ARG] implementation = {implementation}', file=sys.stderr)
_print(f'[CMD-ARG] subcommand = {subcommand}', file=sys.stderr)
_print(f'[CMD-ARG] input_filename = {input_filename}', file=sys.stderr)
_print(f'[CMD-ARG] output_filename = {output_filename}', file=sys.stderr)
_print(f'[CMD-ARG] max_missing = {max_missing}', file=sys.stderr)
_print(f'[CMD-ARG] is_input_sorted = {is_input_sorted}', file=sys.stderr)


my_script_path = os.path.abspath(__file__)
my_script_dir = os.path.dirname(my_script_path)

start_time = time.time()
_print('[PYTHON-START] ' + time.ctime(), file=sys.stderr)

if implementation.lower() == 'python':
	script_path = os.path.join(my_script_dir, 'Python', 'TrieDedup.py')
	command = f'python {script_path} --function {subcommand} --max_missing {max_missing}'
	if is_input_sorted:
		command += ' --sorted'
	command += f' --input {input_filename}'
	if output_filename != '':
		command += f' >{output_filename}.txt'
	check_file_then_exec_command([f'{output_filename}.txt', output_filename], command, True, True, False)
	
	command = f'seqtk subseq {input_filename} {output_filename}.txt >{output_filename}'
	check_file_then_exec_command([output_filename], command, True, True, False)
	
	check_final_file_then_remove_intermediate_file([output_filename], [f'{output_filename}.txt'])
	
elif implementation.lower() == 'java':
	script_path = os.path.join(my_script_dir, 'Java', 'TrieDedup.jar')
	command = f'java -jar {script_path} {subcommand} -m {max_missing}'
	if is_input_sorted:
		command += ' -s'
	if output_filename != '':
		command += f' -o {output_filename}'
	command += f' {input_filename}'
	check_file_then_exec_command([output_filename], command, True, True, False)
elif implementation.lower() == 'cpp':
	script_path = os.path.join(my_script_dir, 'Cpp', 'bin', 'TrieDedup')
	command = f'{script_path} {subcommand} -m {max_missing}'
	if is_input_sorted:
		command += ' -s'
	if output_filename != '':
		command += f' -o {output_filename}'
	command += f' {input_filename}'
	check_file_then_exec_command([output_filename], command, True, True, False)
else:
	die('Error: unrecognized implementation "{implementation}"' + ", which should be one of 'cpp', 'java' or 'python'" + usage)

_print('[PYTHON-END] ' + time.ctime(), file=sys.stderr)
check_elapsed_time(start_time)
