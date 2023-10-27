import sys, os
sys.path.append(f'{os.path.dirname(__file__)}/..')

from argparser import ArgParser


class TestArgParser:
    def _settings(self):
        self.arg_parser = ArgParser()
        self.rules_1 = {
            'pairs':  {                             # Use:
                'Arg 1': ['-i', '--input'],         # -i value, --input value
                'Arg 2': '-r',                      # -r value
                'Wordlist': '-w'                    # -w value
            },
            'single': {  # Take only True or False values
                'Arg 3': ['-n', '--name'],          # -n, --name
                'Arg 4': '-a',                      # -a
                'Arg 5': 'reduce'                   # val
            },
            'united': {
                # -vn=value, --valname:value
                'Arg 6': ('-o', '--output'),
                'Arg 7': '-dn',                     # -dn= value
                # -xn: value, -xname = value, xn : value
                'Arg 8': ['-xn', '-xname', 'xn'],
                'Wordlist': '-w'                    # -w = value
                # (-w alternative value to -w in 'pairs' rules)
            }
        }
        self.rules_2 = {
            'pairs':  {
                'Filename': ['-f', '--filename'],
                'Output': ['-o', '--output'],
                'Title': '-t',
                'Wordlist': ('-w', '--wordlist')
            },
            'single': {  # Take only True or False values
                'Encode': ['-e', 'encode'],
                'EOF': 'EOF',
                'Silent': ['-s', '--silent', 's', 'silent']
            }
        }
        self.rules_3 = {
            'pairs': {
                'JWT': ['--jwt', '--token', '-t', '-jwt']
            }
        }

    def test_arguments_parser_string_1(self):
        self._settings()
        expected_arguments = {'-i': 'file.txt',
                              'reduce': True, '-o': 'output.txt'}
        excpected_ignoreds = ('asdfg',)
        args = '-i file.txt reduce -o: output.txt asdfg'

        arguments, ignoreds = self.arg_parser.parser(self.rules_1, args)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_string_2(self):
        self._settings()
        expected_arguments = {'-w': 'wordlist', '-xn': 'xD', '-a': True,
                              '-dn': 'A B C values'}
        excpected_ignoreds = ()
        args = '-w wordlist -xn = xD -a -dn="A B C values"'

        arguments, ignoreds = self.arg_parser.parser(self.rules_1, args)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_string_3(self):
        self._settings()
        expected_arguments = {
            'Filename': ('--filename', 'file name.txt'),
            'EOF': ('EOF', True),
            'Title': ('-t', 'Hola Mundo!'),
            'Output': ('-o', 'output.txt')
        }
        excpected_ignoreds = ('other_word', 'unknown_value')
        args = '--filename "file name.txt" EOF other_word -t "Hola Mundo!" -o output.txt unknown_value'

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_2, args, wn=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_list_1(self):
        self._settings()
        expected_arguments = {'-w': 'wordlist', '-xn': 'xD', '-a': True,
                              '-dn': 'A B C values'}
        excpected_ignoreds = ()
        args = ['-w', 'wordlist', '-xn', '=',
                'xD', '-a', '-dn=', 'A B C values']

        arguments, ignoreds = self.arg_parser.parser(self.rules_1, args)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_list_2(self):
        self._settings()
        expected_arguments = {
            'Encode': ('-e', True),
            'Filename': ('--filename', 'file name.txt'),
            'Silent': ('--silent', True),
            'Title': ('-t', 'Hola Mundo!'),
            'Wordlist': ('-w', 'wordlist'),
            'Output': ('-o', 'output.txt')
        }
        excpected_ignoreds = ('xD',)
        args = ['-e', '--filename', 'file name.txt', 'xD', '--silent',
                '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_2, args, wasv=False, wn=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_list_3(self):
        self._settings()

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_3, sys.argv)

        assert isinstance(arguments, dict)
        assert isinstance(ignoreds, tuple)

    def test_arguments_parser_repeated_1(self):
        self._settings()
        expected_arguments = {
            'JWT': ('-t', 'asdasdasd')
        }
        excpected_ignoreds = ('-jwt', 'asd', '-jwt', 'asdasd', '--token', 'asdasd')
        args = ['-t', 'asdasdasd', '-jwt', 'asd',
                '-jwt', 'asdasd', '--token', 'asdasd']

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_3, args, wasv=False, wn=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_repeated_2(self):
        self._settings()
        expected_arguments = {
            '-t': 'asdasdasd'
        }
        excpected_ignoreds = ('-jwt', 'asd', '-jwt', 'asdasd', '--token', 'asdasd')
        args = ['-t', 'asdasdasd', '-jwt', 'asd',
                '-jwt', 'asdasd', '--token', 'asdasd']

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_3, args, wasv=False)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

    def test_arguments_parser_repeated_3(self):
        self._settings()
        expected_arguments = {
            '-t': 'asdasdasd'
        }
        excpected_ignoreds = ('-jwt', 'asd', '-jwt', 'asdasd', '--token', 'asdasd')
        args = '-t asdasdasd -jwt asd -jwt asdasd --token asdasd'

        arguments, ignoreds = \
            self.arg_parser.parser(self.rules_3, args, wasv=False)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds
