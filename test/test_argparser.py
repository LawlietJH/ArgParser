import sys, os
sys.path.append(f'{os.path.dirname(__file__)}/..')

from argparser import ArgParser


class TestArgParser:
    def _settings(self):
        self.arg_parser = ArgParser()
        self.rules_1 = {
            'pairs':  { # Key Value                  # Use examples:
                'Key 1': ['-i', '--input'],          # -i value, --input value
                'Key 2': '-r',                       # -r value, -r = value, -r value
                'Key 3': ('-o', '--output'),         # -o=value, --output:value
                'Key 4': '-dn',                      # -dn= value, -dn value, -dn =value
                'Key 5': ['-xn', '-xname', 'xn'],    # -xn: value, -xname = value, xn : value
                'Key 6': '-w'                        # -w value, -w=value, -w:value, -w :value
            },
            'single': { # Bool
                'Key 7': ['-n', '--name'],          # -n, --name
                'Key 8': '-a',                      # -a
                'Key 9': 'reduce'                   # val
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
        self.rules_4 = {
            'single': {
                'JWT': ['--jwt', '--token', '-t', '-jwt']
            }
        }

    def test_arguments_parser_string(self):
        self._settings()
        expected_arguments = {
            '-i': 'file.txt',
            'reduce': True,
            '-o': 'output.txt'
        }
        excpected_ignoreds = ('asdfg',)
        args = '-i file.txt reduce -o: output.txt asdfg'

        arguments, ignoreds = self.arg_parser.parser(args, self.rules_1, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

        expected_arguments = {
            '-w': 'wordlist',
            '-xn': 'xD',
            '-a': True,
            '-dn': 'A B C values'
        }
        args = '-w wordlist -xn = xD -a -dn="A B C values"'

        arguments = self.arg_parser.parser(args)

        assert arguments == expected_arguments

        expected_arguments = {
            'Filename': ('--filename', 'file name.txt'),
            'EOF': ('EOF', True),
            'Title': ('-t', 'Hola Mundo!'),
            'Output': ('-o', 'output.txt')
        }
        excpected_ignoreds = ('other_word', 'unknown_value')
        args = '--filename "file name.txt" EOF other_word -t "Hola Mundo!" -o output.txt unknown_value'

        arguments = self.arg_parser.parser(args, self.rules_2, keys=True)

        assert arguments == expected_arguments

    def test_arguments_parser_list(self):
        self._settings()
        expected_arguments = {
            '-w': 'wordlist',
            '-xn': 'xD',
            '-a': True,
            '-dn': 'A B C values'}
        args = ['-w', 'wordlist', '-xn', '=',
                'xD', '-a', '-dn=', 'A B C values']

        arguments = self.arg_parser.parser(args, self.rules_1)

        assert arguments == expected_arguments

        expected_arguments = {
            'Encode': ('-e', True),
            'Filename': ('--filename', 'file name.txt'),
            'Title': ('-t', 'Hola Mundo!'),
            'Wordlist': ('-w', 'wordlist'),
            'Output': ('-o', 'output.txt')
        }
        excpected_ignoreds = ('xD',)
        args = ['-e', '--filename', 'file name.txt', 'xD',
                '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']

        arguments, ignoreds = \
            self.arg_parser.parser(args, self.rules_2, keys=True, wasv=False, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

        expected_arguments = {
            'Encode': ('-e', True),
            'Filename': ('--filename', 'file name.txt'),
            'Title': ('-t', 'Hola Mundo!'),
            'Wordlist': ('-w', 'wordlist'),
            'Output': ('-o', 'output.txt'),
            'EOF': ('EOF', False),
            'Silent': ('-s', False)
        }
        excpected_ignoreds = ('xD',)
        args = ['-e', '--filename', 'file name.txt', 'xD',
                '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']

        arguments, ignoreds = \
            self.arg_parser.parser(args, keys=True, wasv=True, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

        arguments = self.arg_parser.parser(sys.argv, self.rules_3)

        assert isinstance(arguments, dict)

    def test_arguments_parser_repeated(self):
        self._settings()
        expected_arguments = {
            'JWT': ('-t', 'asdasdasd')
        }
        excpected_ignoreds = ('-jwt', 'asd', '-jwt', 'asdasd', '--token', 'asdasd')
        args = ['-t', 'asdasdasd', '-jwt', 'asd',
                '-jwt', 'asdasd', '--token', 'asdasd']

        arguments, ignoreds = \
            self.arg_parser.parser(args, self.rules_3, keys=True, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

        expected_arguments = {
            '-t': 'asdasdasd'
        }

        arguments = self.arg_parser.parser(args)

        assert arguments == expected_arguments

        args = '-t asdasdasd -jwt asd -jwt asdasd --token asdasd'

        arguments = self.arg_parser.parser(args)

        assert arguments == expected_arguments

    def test_arguments_parser_repeated_single(self):
        self._settings()
        expected_arguments = {
            '-t': True
        }
        excpected_ignoreds = ('-jwt', '-jwt', '--token')
        args = '-t -jwt -jwt --token'

        arguments, ignoreds = \
            self.arg_parser.parser(args, self.rules_4, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds

        expected_arguments = {
            '--token': True
        }
        excpected_ignoreds = ('asdasd', '-jwt', 'asd', '-jwt', '-t', 'xD')
        args = '--token asdasd -jwt asd -jwt -t xD'

        arguments = self.arg_parser.parser(args)

        assert arguments == expected_arguments

        arguments = self.arg_parser.parser()

        assert arguments == expected_arguments

    def test_arguments_parser_class_rules(self):
        self._settings()
        arg_parser = ArgParser(self.rules_4)
        expected_arguments = {
            '--token': True
        }
        excpected_ignoreds = ('asdasd', '-jwt', 'asd', '-jwt', '-t', 'xD')
        args = '--token asdasd -jwt asd -jwt -t xD'

        arguments, ignoreds = arg_parser.parser(args, ignored=True)

        assert arguments == expected_arguments
        assert ignoreds == excpected_ignoreds
