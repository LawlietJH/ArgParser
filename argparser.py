# Tested in: Python 3.8.8
# By: LawlietJH
# ArgParser v1.0.0
# Descripción: Módulo para análisis y extracción de argumentos.
#              Permite mediante reglas obtener valores de los argumentos.
#              Permite analizar una cadena o una lista/tupla de
#              argumentos (como 'sys.argv' así directamente).

import sys

#=======================================================================
__author__  = 'LawlietJH'   # Desarrollador
__title__   = 'ArgParser'   # Nombre
__version__ = 'v1.0.0'      # Version
#=======================================================================

class ArgParser:
	
	class MissingArgument(Exception):
		def __init__(self, error_msg=''): self.error_msg = error_msg
		def __str__(self): return repr(self.error_msg)
	
	def __init__(self, rules=None, args=None, wasv=None, wn=None):
		self.rules = rules	# Rules for parsing arguments.
		self.args  = args	# Arguments to parse.
		self.wasv  = wasv	# output with all single values (true and false).
		self.wn    = wn		# output with names: {'Name': ('argument', 'value')}.
		self.help  = '''Example...\n
		\r rules = {
		\r     'pairs':  {  # 'arg value'               # Use:
		\r         'Name 1': ['-e', '--example'],       # -e value, --example value
		\r         'Name 2': '-o',                      # -o value
		\r         'Wordlist': '-w'                     # -w value
		\r     },
		\r     'single': {  # 'arg'
		\r         'Name 3': ['-n', '--name'],          # -n, --name
		\r         'Name 4': '-a',                      # -a
		\r         'Name 5': 'val'                      # val
		\r     },
		\r     'united': {  # 'arg = value' or 'arg: value'
		\r         'Name 6': ('-vn', '--valuename'),    # -vn=value, --valname:value
		\r         'Name 7': '-dn',                     # -dn= value
		\r         'Name 8': ['-xn', '-xname', 'xn'],   # -xn: value, -xname = value, xn : value
		\r         'Wordlist': '-w'                     # -w: value
		\r                                              # (-w alternative value to -w in 'pairs' rules)
		\r     }
		\r }
		'''
	
	def __call__(self, rules=None, args=None, wasv=None, wn=None):
		if not self.rules:
			if not rules:
				raise self.MissingArgument("El argumento 'rules' es obligatorio.")
			else:
				self.rules = rules
		else:
			self.rules = rules
		if not self.args:
			if not args:
				raise self.MissingArgument("El argumento 'args' es obligatorio.")
			else:
				self.args = args
		else:
			self.args = args
		
		if not self.wasv and wasv:
			self.wasv = wasv
		if not self.wn and wn:
			self.wn = wn
		
		return self.parser(self.rules, self.args, self.wasv, self.wn)
	
	def pairsUnion(self, args):
		
		# Union of params with '=' or ':'
		tmp = []
		concat = ''
		
		for i, arg in enumerate(args):
			try:
				if i+1 < len(args) and args[i+1] == '=':
					concat += arg
					continue
				elif arg == '=':
					concat += arg
					continue
				elif i > 0 and args[i-1] == '=':
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			try:
				if i+1 < len(args) and args[i+1] == ':':
					concat += arg
					continue
				elif arg == ':':
					concat += arg
					continue
				elif args[i-1] == ':':
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			try:
				if i+1 < len(args) and args[i+1].startswith('='):
					concat += arg
					continue
				elif arg.startswith('='):
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			try:
				if i+1 < len(args) and args[i+1].startswith(':'):
					concat += arg
					continue
				elif arg.startswith(':'):
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			try:
				if arg.endswith('='):
					concat += arg
					continue
				elif i > 0 and args[i-1].endswith('='):
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			try:
				if arg.endswith(':'):
					concat += arg
					continue
				elif i > 0 and args[i-1].endswith(':'):
					concat += arg
					tmp.append(concat)
					concat = ''
					continue
			except: pass
			
			if concat:
				tmp.append(concat)
				concat = ''
			else:
				tmp.append(arg)
		
		args = tmp
		
		return args
	
	def pairsVals(self, arg, args, pairs, output, wn):
		
		ignore = True
		
		for key, val in pairs.items():
			
			if val.__class__ in [list, tuple]:
				if arg in val:
					if wn and not key in output:
						output[key] = (arg, args.pop(0))
					elif not arg in output:
						output[arg] = args.pop(0)
					ignore = False
					break
			elif val.__class__ == str:
				if arg == val:
					try:
						if wn and not key in output:
							output[key] = (arg, args.pop(0))
						elif not arg in output:
							output[arg] = args.pop(0)
					except:
						break
					ignore = False
					break
		
		return ignore
	
	def singleVals(self, arg, single, output, wn):
		
		ignore = True
		
		for key, val in single.items():
			
			if val.__class__ in [list, tuple]:
				if arg in val:
					if wn:
						output[key] = (arg, True)
					else:
						output[arg] = True
					ignore = False
					break
			elif val.__class__ == str:
				if arg == val:
					if wn:
						output[key] = (arg, True)
					else:
						output[arg] = True
					ignore = False
					break
		
		return ignore
	
	def unitedVals(self, arg, united, output, ignored, wn):
		
		tmp_arg = arg.split(':')
		if len(tmp_arg) != 2:
			tmp_arg = tmp_arg[0].split('=')
			if len(tmp_arg) != 2:
				ignored.append(arg)
				return 'continue'
		
		ignore = True
		
		for key, val in united.items():
			
			if val.__class__ in [list, tuple]:
				if tmp_arg[0] in val:
					if wn and not key in output:
						output[key] = (tmp_arg[0], tmp_arg[1])
					elif not tmp_arg[0] in output:
						output[tmp_arg[0]] = tmp_arg[1]
					ignore = False
					break
			elif val.__class__ == str:
				if tmp_arg[0] == val:
					if wn and not key in output:
						output[key] = (tmp_arg[0], tmp_arg[1])
					elif not tmp_arg[0] in output:
						output[tmp_arg[0]] = tmp_arg[1]
					ignore = False
					break
		
		return ignore
	
	def stringsParser(self, args):
		tmp = []
		init = False
		char = ''
		for arg in args:
			if (arg.startswith('"') or arg.startswith("'")) \
			and not ('"' in arg[1:] or "'" in arg[1:]) and not init:
				tmp.append(arg[1:])
				init = True
				if arg.startswith('"'): char = '"'
				else: char = "'"
			elif (arg.startswith('="') or arg.startswith("='")) and not init:
				tmp.append('='+arg[2:])
				init = True
				if arg.startswith('="'): char = '"'
				else: char = "'"
			elif ('="' in arg or "='" in arg) and not init:
				if '="' in arg:
					arg = arg.replace('="', '=')
					char = '"'
				else:
					arg = arg.replace("='", '=')
					char = "'"
				tmp.append(arg)
				init = True
			elif (arg.startswith('"') or arg.startswith("'")) and not init:
				tmp.append(arg[1:])
				init = True
				if arg.startswith('"'): char = '"'
				else: char = "'"
			elif (arg.endswith('"') or arg.endswith("'")) and init:
				tmp[-1] += ' ' + arg[:-1]
				init = False
				if arg.endswith('"'): char = '"'
				else: char = "'"
			elif init:
				tmp[-1] += ' ' + arg
			else:
				if char == '"':
					arg = arg.replace('"', '')
				else:
					arg = arg.replace("'", '')
				tmp.append(arg)
		return tmp
	
	def parser(self, rules, args, wasv=False, wn=False):
		# rules -> Rules for parsing arguments.
		# args  -> Arguments to parse.
		# wasv  -> output with all single values (true and false).
		# wn    -> output with names: {'Name': ('argument', 'value')}.
		
		ignored = []
		output = {}
		
		assert rules.__class__ == dict, self.help
		
		pairs  = rules.get('pairs')
		single = rules.get('single')
		united = rules.get('united')
		
		assert pairs or single or united, self.help
		
		if args.__class__ == str:
			args = args.split(' ')
		if args.__class__ == tuple:
			args = list(args)
		if args.__class__ == list:
			# ~ while '' in args:
				# ~ args.remove('')
			tmp = []
			for arg in args:
				if ' ' in arg and not ('="' in arg or "='" in arg) and \
				(not (arg.startswith('"') and arg.endswith('"')) or \
				(not (arg.startswith("'") and arg.endswith("'")))):
					arg = '"' + arg + '"'
				arg = arg.split(' ')
				tmp.extend(arg)
			args = tmp
		
		# Argument String Parser:
		args = self.stringsParser(args)
		
		assert args.__class__ == list, f'args = {args} is not valid.'
		
		args = self.pairsUnion(args)
		
		while args:
			
			arg = args.pop(0)
			ignore = True
			
			if pairs: # Validate Pairs: -Arg Value
				ignore = self.pairsVals(arg, args, pairs, output, wn)
			
			if ignore:
				
				if single: # Validate Single: -Arg
					ignore = self.singleVals(arg, single, output, wn)
				
				if ignore:
					
					if united: # Validate United: -Arg = Value, -Arg: Value
						ignore = self.unitedVals(arg, united, output, ignored, wn)
					
					if ignore == 'continue':
						continue
					
					if ignore:
						ignored.append(arg)
		
		if single and wn and wasv:
			arguments = [argument for argument, content in output.values()]
			print(arguments)
			for key, value in single.items():
				print(key, value)
				if value.__class__ in (list, tuple):
					in_output = [False, value[0]]
					for val in value:
						if val in arguments:
							in_output = [True, val]
							break
					if not in_output[0]:
						output[key] = (in_output[1], False)
				elif not key in arguments:
					output[key] = (value, False)
		elif single and not wn and wasv:
			for value in single.values():
				if value.__class__ in (list, tuple):
					in_output = [False, value[0]]
					for val in value:
						if val in output:
							in_output = [True, val]
							break
					if not in_output[0]:
						output[in_output[1]] = False
				elif not value in output:
					output[value] = False
		
		# Reset params:
		self.wasv = None
		self.wn   = None
		
		return output, tuple(ignored)	# Output Values with Arguments and Values Ignored.



if __name__ == '__main__':
	
	# Usage Examples:
	
	argParser = ArgParser()
	
	#-------------------------------------------------------------------
	# Example #1:
	rules = {
		'pairs':  {                             # Use:
			'Arg 1': ['-i', '--input'],         # -i value, --input value
			'Arg 2': '-r',                      # -r value
			'Wordlist': '-w'                    # -w value
		},
		'single': { # Take only True or False values
			'Arg 3': ['-n', '--name'],          # -n, --name
			'Arg 4': '-a',                      # -a
			'Arg 5': 'reduce'                   # val
		},
		'united': {
			'Arg 6': ('-o', '--output'),        # -vn=value, --valname:value
			'Arg 7': '-dn',                     # -dn= value
			'Arg 8': ['-xn', '-xname', 'xn'],   # -xn: value, -xname = value, xn : value
			'Wordlist': '-w'                    # -w = value
			                                    # (-w alternative value to -w in 'pairs' rules)
		}
	}
	
	args = '-i file.txt reduce -o: output.txt asdfg'
	out, ign = argParser(rules, args)
	print(out)		# Output Values with Arguments
	print(ign)		# Values Ignored
	# Output:
	# {'-i': 'file.txt', 'reduce': True, '-o': 'output.txt'}
	# ('asdfg',)
	
	args = '-w wordlist -xn = xD -a -dn="A B C values"'
	out, ign = argParser(rules, args)
	print(out)
	print(ign)
	# Output:
	# {'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
	# ()
	
	# Same example but with a list of arguments
	args = ['-w', 'wordlist', '-xn', '=', 'xD', '-a', '-dn=', 'A B C values']
	out, ign = argParser(rules, args)
	print(out)
	print(ign)
	# Output:
	# {'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
	# ()
	
	#-------------------------------------------------------------------
	# Ejemplo #2:
	rules = {
		'pairs':  {
			'Filename': ['-f', '--filename'],
			'Output':   ['-o', '--output'],
			'Title':     '-t',
			'Wordlist': ('-w', '--wordlist')
		},
		'single': { # Take only True or False values
			'Encode': ['-e', 'encode'],
			'EOF':     'EOF',
			'Silent': ['-s', '--silent', 's', 'silent']
		}
	}
	
	args = '--filename "file name.txt" EOF other_word -t "Hola Mundo!" -o output.txt unknown_value'
	out, ign = argParser(rules, args, wn=True)
	print(out)
	print(ign)
	# Output:
	# {
	#     'Filename': ('--filename', 'file name.txt'),
	#     'EOF':      ('EOF', True),
	#     'Title':    ('-t', 'Hola Mundo!'),
	#     'Output':   ('-o', 'output.txt')
	# }
	# ('other_word', 'unknown_value')
	
	args = ['-e', '--filename', 'file name.txt', 'xD', '--silent', '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']
	out, ign = argParser(rules, args, wasv=False, wn=True)
	print(out)
	print(ign)
	# Output:
	# {
	#     'Encode':   ('-e', True),
	#     'Filename': ('--filename', 'file name.txt'),
	#     'Silent':   ('--silent', True),
	#     'Title':    ('-t', 'Hola Mundo!'),
	#     'Wordlist': ('-w', 'wordlist'),
	#     'Output':   ('-o', 'output.txt')
	# }
	# ('xD',)
	
	# Parse Script Arguments -------------------------------------------
	out, ign = argParser(rules, sys.argv)
	print(out)
	print(ign)
	# Output:
	# {'-f': 'file.txt', '-o': 'output_file.txt'}
	# ('argparser.py',)
