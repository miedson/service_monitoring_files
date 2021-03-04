# Serviço de monitoramento de arquivos
O serviço é responsavel por monitorar a importação de arquivos em determinado diretorio FTP durante um intervalo de tempo, se nenhum arquivo chegar, o serviço enviar e-mails de alerta dobrando esse tempo de espera até que um novo arquivo chegue. 

No arquivo de Config é possivel determinar todas as configurações necessarias:

//HORARIO DE SEGUNDA E SEXTA

start=07:15
end=18:00

//HORARIO FIM DE SEMANA

startFds=00:00
endFds=00:01

//CAMINHO DO DIRETÓRIO A SER MONITORADO
path=

//TEMPO DE ESPERA ATÉ A CHEGADA DE NOVO ARQUIVO E INTERVALO DE ENVIO DE E-MAILs
tempo=1

//TEMPO DE ESPERA FIM DE SEMANA
tempoFds=10

//QUANTIDADE DE E-MAILs A SEREM DISPARADOS POR TEMPO DE ESPERA
emails=1

//CAMINHO PARA SALVAR OS LOGs
log=

//CONFIGURAÇÕES DO SERVIDOR DE E-MAIL
smtp_host=
smtp_port=
user=
password=

//DADOS DO E-MAIL
emailTo=email1, e-mail2
subject=Titulo do e-mail
body=Mensagem do e-mail
