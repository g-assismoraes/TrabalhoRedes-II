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
<p>Ao iniciar o módulo cliente deve-se informar seu nome e o endereço IPV4 que será utilizado para estabelecer a conexão.</p>
<p>Caso seja digitado um novo nome de usuário, será realizado o registro.</p> 
<p>Caso contrário, o usuário será informado que houve falha no registro.</p>

<hr>

<h2> FUNCIONALIDADES </h2>
  
Após o registro, o usuário deverá informar se deseja encerrar a conexão[^1] ou se deseja consultar a tabela de registro do servidor [^2].  

[^1]: Para isso utiliza-se o dígito 0.
[^2]: Para isso utiliza-se o dígito 1.
  
<h6>CONSULTA DE REGISTRO</h6>

Após digitar um nome que conste na tabela de registro do servidor e esse enviar uma resposta bem sucedida, será enviada uma mensagem ao destinatário solicitando uma conexão UDP entre eles. [^3].  

[^3]: Para aceitar, o destinatário deverá responder com a tecla Y, do contrário, com a tecla N.
  
Ao aceitar a conexão será apresentada uma mensagem indicando qual tecla utilizar para encerrar a conexão e será iniciada a transmissão síncrona de áudio.
  
Caso o nome solicitado não conste na tabela de registro do servidor o remetente será informado e poderá escolher novamente se deseja encerrar a conexão ou consultar a tabela de registro do servidor.
  
<h6>ENCERRAR CONEXÃO</h6>
<li>Enquanto o usuário não estiver em uma chamada, a conexão pode ser encerrada através do dígito 0.
<li>Enquanto o usuário estiver em uma chamada, essa deve ser encerrada primeiro por meio da tecla indicada no início para então se encerrar a conexão. 
<p> </p>
