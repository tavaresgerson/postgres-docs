## 44.11. Variáveis de ambiente [#](#PLPYTHON-ENVAR)

Algumas das variáveis de ambiente que são aceitas pelo interpretador Python também podem ser usadas para afetar o comportamento do PL/Python. Elas precisam ser definidas no ambiente do processo do servidor PostgreSQL principal, por exemplo, em um script de inicialização. As variáveis de ambiente disponíveis dependem da versão do Python; consulte a documentação do Python para detalhes. No momento em que este texto é escrito, as seguintes variáveis de ambiente têm efeito no PL/Python, assumindo uma versão adequada do Python:

* `PYTHONHOME`
* `PYTHONPATH`
* `PYTHONY2K`
* `PYTHONOPTIMIZE`
* `PYTHONDEBUG`
* `PYTHONVERBOSE`
* `PYTHONCASEOK`
* `PYTHONDONTWRITEBYTECODE`
* `PYTHONIOENCODING`
* `PYTHONUSERBASE`
* `PYTHONHASHSEED`

(Aparece ser um detalhe da implementação do Python que está além do controle do PL/Python, e que algumas das variáveis de ambiente listadas na página de manual `python` só são eficazes em um interpretador de linha de comando e não em um interpretador Python embutido.)