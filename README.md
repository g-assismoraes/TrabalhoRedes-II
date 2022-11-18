<h1 align="center">PROJETO</h1>

Projeto de aplicação que utiliza o paradigma cliente-servidor e socket de rede para simular uma sala virtual de conversa.

<hr>

<h4>DETALHES</h3

1. A conversa será realizada apenas entre dois usuários e ocorrerá por meio de transmissão síncrona de áudio.
2. Uma vez que um usuário está registrado no servidor, pode realizar uma ligação para qualquer outro usuário que também esteja registrado.

<hr>

<h2> INICIANDO A APLICAÇÃO </h2>

Para o correto funcionamento da aplicação deve-se:

<li>Iniciar o servidor TCP (servidorTCP.py);
<li>Iniciar um cliente TCP (controller.py).
<h6>OBSERVAÇÃO</h6>
Em casos de teste onde apenas uma máquina é utilizada para a execução da aplicação, deve-se a cada nova execução do cliente:
<li>Utilizar outro nome;
<li>Utilizar outra porta;
<li>Utilizar outra tecla responsável por cancelar a conexão a qualquer momento.

<hr>

<h2> FUNCIONAMENTO DA APLICAÇÃO </h2>

<h6>SERVIDOR</h6>
<p>Após iniciado o servidor TCP, o mesmo permanece aguardando pedidos de conexão dos clientes</p>
<p>Além disso, o servidor exibe uma mensagem na qual constam o endereço IPV4 e a porta em que está conectado.</p>
<p>Ao receber dados de um usuário o servidor:</p>
<li>Adiciona os dados do usuário à sua tabela de registros, caso seja um novo usuário;
<li>Caso contrário, informa ao usuário que o usuário já está registrado.

<h6>CLIENTE</h6>
<p>Ao iniciar o módulo cliente deve-se informar nome, IP e porta que serão utilizados para estabelecer a conexão.</p>

<hr>

<h2> FUNCIONALIDADES </h2>
<h6>CONSULTA DE REGISTRO</h6>


