import string
import base64
import sys
from secrets import SystemRandom


def get_secretkey():
    secretkey = ''.join(
        SystemRandom().choices(
            string.ascii_letters
            + string.digits
            + string.punctuation,
            k=64
        )
    )
    if '"' in secretkey or '"' in secretkey:
        return get_secretkey()
    else:
        return secretkey


def get_base64(nome='.env', secretkey=False):
    with open(f'./dotenv_files/{nome}') as arquivo:
        texto = arquivo.read()

    if secretkey:
        texto = texto.replace(
            'SECRET_KEY="django-insecure-u8-^&u+70c^ak7bf5!4r$2v__y1f_5&9p#0)my_=ho2b+8)inq"',
            f'SECRET_KEY="{get_secretkey()}"'
        )
    base64_convertido = base64.b64encode(texto.encode())

    return base64_convertido.decode()


def help():
    return """

python env.py [COMANDOS]

COMANDOS:
    -secretkey          Para pegar uma chave Secreta.
    -base64             Para pegar as chaves em base64.
        -e <nome>       Para indicar o nome do arquivo.
        -s True         Para que seja trocado o SECRET_KEY antes de 
                        converter para base64.
    --help | -h              Para pedir ajuda.
"""


resultado = sys.argv[1:]

entrada = {}

if "-secretkey" in resultado:
    print(get_secretkey())

elif "-base64" in resultado:
    if '-e' in resultado:
        entrada['nome'] = resultado[resultado.index('-e')+1]

    if '-s' in resultado:
        secretkey = resultado[resultado.index('-s')+1]
        if secretkey == 'True':
            entrada['secretkey'] = True

    print(get_base64(**entrada))
elif "-h" in resultado or "--help" in resultado:
    print(help())
else:
    print(help())
