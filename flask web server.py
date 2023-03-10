from flask import Flask, request, render_template
import json
from flask import jsonify
import time
import paramiko


# test 1 = testa se arg1 está vazio, aceita label.
def test1(testvar, label=""):
    def logictest(var):
        if var == "":
            return True
        else:
            return False
    
    if label: # quer retorno
        if logictest(testvar):
            return print(f"[{label}] Sem conteúdo.")
        else:
            return print(f"[{label}] Há conteúdo. ({testvar})")
    else:
        return logictest(testvar)
        
# test 2 = testa se arg1 é igual a arg2, aceita label
def test2(testvar, comparator, label=""):
    def logictest(var):
        if var == comparator:
            return True
        else:
            return False
    
    if label: # quer retorno
        if logictest(testvar):
            return print(f"[{label}] Igual.")
        else:
            return print(f"[{label}] Diferente.")
    else:
        return logictest(testvar)

# Para redirecionar à outro path da URL
def redirectTo(path, *args, **kwargs):
    try: 
        msg=kwargs['mensagem']
    except KeyError:
        pass # Não importa se passar a mensagem ou não.
    finally:
        print("deu certo")
    
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    return f'<script>window.location.assign("{path}")</script>'

def sshcommit(comando):
    print(f'> "{comando}"...')
    stdin, stdout, stderr = client.exec_command(comando, get_pty=True)
    resultpmk = stdout.read().decode('utf-8')
    erro = 'Erro!'
    if stdout.channel.recv_exit_status() == 0:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    else:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    if "Permission denied" in resultpmk:
        print('PERMISSION DENIED!')
        print(f'{resultpmk}')
        stdin.close()
        stdout.close()
        stderr.close()
        return erro
    else:
        stdin.close()
        stdout.close()
        stderr.close()
        return resultpmk


app = Flask(__name__)

@app.route("/")
def main():
    return """<p>TESTE</p>"""

@app.route("/erro")
def erro():
    return render_template("erro.html")

@app.route("/zbx", methods=['GET', 'POST'])
def mytest():
    
    if request.method =='POST': # se o método for POST, vou tratar os valores recebidos e exibir a página de resultado para POST
        
        key = "C:\\Users\\Operação 16\\.ssh\\id_rsa.pub"
                   
        zabbix_server_ip = request.form['zabbix_ip']
        zabbix_hostname = request.form['zabbix_host_name']
        host_ip = request.form['host_ip']
        host_port = 22 if request.form['host_port'] == '' else request.form['host_port']
        host_user = request.form['host_user']
        host_pass = request.form['host_pass']
        host_key = request.form['host_key']
        test1(zabbix_server_ip, "z-ip")
        test1(zabbix_hostname, "hostname")
        test1(host_ip, "h-ip")
        test1(host_port, "port")
        test1(host_user, "user")
        test1(host_pass, "pass")
        test1(host_key, "key")

        # Abrindo o processo SSH PARAMIKO
        client = paramiko.client.SSHClient()
        # Aceitando/adicionando a KEY
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print('\n-- CONEXÃO PARAMIKO (SSH) --')
            client.connect(host_ip, username=host_user, password=host_pass, port=host_port, key_filename=key)
        except Exception as e:
            client.close()
            print(f"falha ao se conectar...")
            print(e)
            return redirectTo("/erro", _type="ssh", _erro=e)
        else:
            # conexao bem sucedida
            return f'''<h1>Conexão bem sucedida!</h1>
<h3>Zabbix Server IP: {zabbix_server_ip}</h3>
<h3>Zabbix Hostname: {zabbix_hostname}</h3>
<h3>Host IP: {host_ip}</h3>
<h3>Host Port: {host_port}</h3>
<h3>Host User: {host_user}</h3>
<h3>Host Pass: {host_pass}</h3>'''
        
    elif request.method =='GET':
        return render_template('start_menu.html')
    else:
        redirectTo("/erro")

if __name__ == "__main__":
    app.run()
    
# rodar no terminal 
# flask --app "[nome arquivo]" run
# após, dar CTRL C no terminal p/ parar o server