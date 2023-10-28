# ArgParser
 Módulo para análisis y extracción de argumentos. Permite mediante reglas obtener valores de los argumentos. Permite analizar una cadena o una lista/tupla de argumentos (como 'sys.argv' así directamente).

## v1.0.4

Debes crear un diccionario de reglas. Debe contener al menos 1 de los 2 tipos de reglas permitidas, cada tipo de regla contendrá los nombres (Key) de los argumentos.

Los tipos de reglas son:

* Pairs: Cada argumento esperará recibir un segundo valor a su derecha separado al menos por un espacio o por un signo '=' o ':'.
* Single: Cada argumento irá colocado de forma única y esperará ningún otro valor. Si el argumento es colocado, obtendrá un valor True, si no, False.

Además:

* Los argumentos que no cumplan los requisitos serán asignados como 'Ignored'.
* Si existe uno o más argumentos con la misma regla, solo se tomará en cuenta la primera coincidencia.

## Ejemplos de Uso

Creando tus propias reglas, Ejemplo: Se las podemos pasar a la clase para crear las reglas.

Las Key pueden llevar cualquier nombre.
Los Value pueden ser un string cualquiera o una lista o tupla de strings con longitud ilimitada.

```Python
>>> from argparser import ArgParser
>>> rules = {
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
>>> arg_parser = ArgParser(rules)
```

El parámetro `ignored` nos permite recibir una tupla con los argumentos ignorados por las reglas.

```Python
>>> args = '-i file.txt reduce -o: output.txt asdfg'
>>> out, ign = arg_parser.parser(args, ignored=True)
>>> out    # Output with argument values
{'-i': 'file.txt', 'reduce': True, '-o': 'output.txt'}
>>> ign    # Ignored values
('asdfg',)
```

```Python
>>> args = '-w wordlist -xn = xD -a -dn="A B C values"'
>>> out = arg_parser.parser(args)
>>> out
{'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
```

```Python
>>> # Same example but with a list of arguments
>>> args = ['-w', 'wordlist', '-xn', '=', 'xD', '-a', '-dn=', 'A B C values']
>>> out = arg_parser.parser(args)
>>> out
{'-w': 'wordlist', '-xn': 'xD', '-a': True, '-dn': 'A B C values'}
```

Ejemplo #2:

```Python
rules = {
    'pairs':  {
        'Filename': ['-f', '--filename'],
        'Output':   ['-o', '--output'],
        'Title':     '-t',
        'Wordlist': ('-w', '--wordlist')
    },
    'single': { # The arguments are considered boolean values. True if the argument exists, otherwise False.
        'Encode': ['-e', 'encode'],
        'EOF':     'EOF',
        'Silent': ['-s', '--silent', 's', 'silent']
    } # Use the 'wasv' parameter to get False values too.
}
```

Nota: para actualizar las reglas, se las podemos pasar como un segundo parámetro a la función `parser()`.

Agregando el parámetro 'keys' (With Keys), mostrará en el 'output' los nombres de los argumentos:

```Python
>>> args = '--filename "file name.txt" EOF other_word -t "Hola Mundo!" -o output.txt unknown_value'
>>> out, ign = arg_parser.parser(args, rules=rules, keys=True, ignored=True)
>>> out
{
    'Filename': ('--filename', 'file name.txt'),
    'EOF': ('EOF', True),
    'Title': ('-t', 'Hola Mundo!'),
    'Output': ('-o', 'output.txt')
}
>>> ign
('other_word', 'unknown_value')
```

Agregando el parámetro 'wasv' (With All Single Values), mostrará en el 'output' todos los argumentos con las reglas de tipo 'Single', ya sean True o False:

```Python
>>> args = ['-e', '--filename', 'file name.txt', 'xD', '-t', 'Hola Mundo!', '-w', 'wordlist', '-o', 'output.txt']
>>> out1 = arg_parser.parser(args, keys=True, wasv=False)
>>> out2 = arg_parser.parser(args, keys=True, wasv=True)
>>> out1
{
    'Encode':   ('-e', True),
    'Filename': ('--filename', 'file name.txt'),
    'Title':    ('-t', 'Hola Mundo!'),
    'Wordlist': ('-w', 'wordlist'),
    'Output':   ('-o', 'output.txt')
}
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
out, ign = arg_parser.parser(sys.argv, rules, ignored=True)

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
> python argparser.py -f file.txt word_etc -o output_file.txt
{'-f': 'file.txt', '-o': 'output_file.txt'}
('argparser.py', 'word_etc')
```
