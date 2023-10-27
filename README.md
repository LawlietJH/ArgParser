# ArgParser
 Módulo para análisis y extracción de argumentos. Permite mediante reglas obtener valores de los argumentos. Permite analizar una cadena o una lista/tupla de argumentos (como 'sys.argv' así directamente).

## v1.0.3

Debes crear un diccionario de reglas. Debe contener al menos 1 de los 3 tipos de reglas permitidas, cada tipo de regla contendrá los nombres de los argumentos. 

Los tipos de reglas son:

* Pairs: Cada argumento esperará recibir un segundo valor a su derecha separado al menos por un espacio.
* Single: Cada argumento irá colocado de forma única y esperará ningún otro valor. Si el argumento es colocado, obtendrá un valor True, si no, False.
* United: Cada argumento esperará recibir un segundo valor a su derecha separado por un signo '=' o ':', también puede haber espacios entre estos, pero el signo '=' o ':' es obligatorio.

Además:

* Los argumentos que no cumplan los requisitos serán asignados como 'Ignored'.
* Si existe uno o más argumentos con la misma regla, solo se tomará en cuenta la primera coincidencia.
* Es posible utilizar más de una regla para un mismo tipo de argumento. Esto es, agregando la misma regla a más de uno de los 3 tipos de reglas, de esta forma, podría ser válido, por ejemplo: '-w wordlist' y '-w = wordlist'.

## Ejemplos de Uso

Creando tus propias reglas, Ejemplo: Se las podemos pasar a la clase para crear las reglas.

```Python
>>> from argparser import ArgParser
>>> rules = {
...     'pairs':  {                             # Use:
...         'Arg 1': ['-i', '--input'],         # -i value, --input value
...         'Arg 2': '-r',                      # -r value
...         'Wordlist': '-w'                    # -w value
...     },
...     'single': { # Take only True or False values
...         'Arg 3': ['-n', '--name'],          # -n, --name
...         'Arg 4': '-a',                      # -a
...         'Arg 5': 'reduce'                   # val
...     },
...     'united': {
...         'Arg 6': ('-o', '--output'),        # -vn=value, --valname:value
...         'Arg 7': '-dn',                     # -dn= value
...         'Arg 8': ['-xn', '-xname', 'xn'],   # -xn: value, -xname = value, xn : value
...         'Wordlist': '-w'                    # -w = value
...                                             # (-w alternative value to -w in 'pairs' rules)
...     }
... }
>>> arg_parser = ArgParser(rules)
```

```Python
>>> args = '-i file.txt reduce -o: output.txt asdfg'
>>> out, ign = arg_parser.parser(args)
>>> out    # Output Values with Arguments
{'-i': 'file.txt', 'reduce': True, '-o': 'output.txt'}
>>> ign    # Values Ignored
('asdfg',)
```

```Python
>>> args = '-w wordlist -xn = xD -a -dn="A B C values"'
>>> out, ign = arg_parser.parser(args)
>>> out
{'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
>>> ign
()
```

```Python
>>> # Same example but with a list of arguments
>>> args = ['-w', 'wordlist', '-xn', '=', 'xD', '-a', '-dn=', 'A B C values']
>>> out, ign = arg_parser.parser(args)
>>> out
{'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
>>> ign
()
```

Ejemplo #2:

```Python
... rules = {
...     'pairs':  {
...         'Filename': ['-f', '--filename'],
...         'Output':   ['-o', '--output'],
...         'Title':     '-t',
...         'Wordlist': ('-w', '--wordlist')
...     },
...     'single': { # The arguments are considered boolean values. True if the argument exists, otherwise False.
...         'Encode': ['-e', 'encode'],
...         'EOF':     'EOF',
...         'Silent': ['-s', '--silent', 's', 'silent']
...     } # Use the 'wasv' parameter to get False values.
... }
```

Nota: para actualizar las reglas, se las podemos pasar como un segundo parámetro a la función `parser()`.

Agregando el parámetro 'keys' (With Keys), mostrará en el 'output' los nombres de los argumentos:

```Python
>>> args = '--filename "file name.txt" EOF other_word -t "Hola Mundo!" -o output.txt unknown_value'
>>> out, ign = arg_parser.parser(args, rules=rules, keys=True)
>>> out
{
    'Filename': ('--filename', 'file name.txt'),
    'EOF':      ('EOF', True),
    'Title':    ('-t', 'Hola Mundo!'),
    'Output':   ('-o', 'output.txt')
}
>>> ign
('other_word', 'unknown_value')
```

Agregando el parámetro 'wasv' (With All Single Values), mostrará en el 'output' todos los argumentos con las reglas de tipo 'Single', ya sean True o False:

```Python
>>> args = ['-e', '--filename', 'file name.txt', 'xD', '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']
>>> out1, ign1 = arg_parser.parser(args, wasv=False, keys=True)
>>> out2, ign2 = arg_parser.parser(args, wasv=True, keys=True)
>>> out1
{
    'Encode':   ('-e', True),
    'Filename': ('--filename', 'file name.txt'),
    'Title':    ('-t', 'Hola Mundo!'),
    'Wordlist': ('-w', 'wordlist'),
    'Output':   ('-o', 'output.txt')
}
>>> ign1
('xD',)
>>> out2
{
    'Encode':   ('-e', True),
    'Filename': ('--filename', 'file name.txt'),
    'Title':    ('-t', 'Hola Mundo!'),
    'Wordlist': ('-w', 'wordlist'),
    'Output':   ('-o', 'output.txt'),
    'EOF':      ('EOF', False),
    'Silent':   ('-s', False)
}
>>> ign2
('xD',)
```

Podemos crear la clase sin reglas, pero al utilizar la función `parser()` habrá que actualizar obligatoriamente las reglas utilizando la primera vez un segundo parámetro llamado `rules`.
Utilizando 'sys.argv' para el análisis de argumentos del Script:

```Python
# En el código:
import sys
from argparser import ArgParser

arg_parser = ArgParser()
rules = {
    'pairs':  {
        'Filename': ['-f', '--filename'],
        'Output':   ['-o', '--output']
    }
}
out, ign = arg_parser.parser(sys.argv, rules)

print(out)
print(ign)
```

```Bash
# En la terminal:
> python argparser.py -f file.txt -o output_file.txt
{'-f': 'file.txt', '-o': 'output_file.txt'}
('argparser.py',)
```

```Bash
> python argparser.py -f file.txt etc -o output_file.txt
{'-f': 'file.txt', '-o': 'output_file.txt'}
('argparser.py', 'etc')
```
