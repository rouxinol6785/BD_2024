import flask
import logging
import psycopg2
import jwt
import random
import time


app = flask.Flask(__name__)
jwt_key = "DB_upa"


StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

def db_connection():
    db = psycopg2.connect(
        user='projeto_bd',
        password='password',
        host='127.0.0.1',
        port='5432',
        database='MeDEIsync'
    )

    return db

 # set up logging
logging.basicConfig(filename='log_file.log')
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

@app.route('/')
def landing_page():
    return"""
    Bem-vindo!<br/>
"""

# register patient
@app.route('/MeDEIsync_DB/user/register/patient', methods =['POST'])
def patient_registration():

    logger.info('POST /MeDEIsync_DB/user/register/patient')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/user/registration/patient - payload: {payload}')


    if 'cc'not in payload or 'nome' not in payload or 'password' not in payload or 'data_nascimento' not in payload  or 'medical_record' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = random.randint(0,30)

    statement = 'INSERT INTO use (cc,nome,password,data_nascimento) VALUES(%s,%s,%s,%s)'
    statemnt2 = 'INSERT INTO patient (use_cc, medical_record) VALUES(%s,%s)'

    values = (int (payload['cc']),payload['nome'],payload['password'],payload['data_nascimento'])
    values2 = (int (payload['cc']),payload['medical_record'])
    try:
        cur.execute("SELECT nome FROM use WHERE nome = %s",(payload['nome'],))
        existing_user = cur.fetchone()
        if existing_user:
            response ={
                'status' : StatusCodes['api_error'], 'results': 'Paciente já está na base de dados'}
            conn.close()
            return flask.jsonify(response)
        else:
            #isto sempre no início das transações, se der merda a meio podemos fazer rollback e volta a como estava aqui
            cur.execute("BEGIN TRANSACTION")
            cur.execute(statement,values)
            cur.execute(statemnt2,values2)
            conn.commit()
            response = {
                'status': StatusCodes['success'], 'results': f'Paciente {payload['nome']} inserido!'
            }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/registration/patient - error: {error}')
        response = {
            'status': StatusCodes['internal_error'], 'errors': str(error)
        }
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# User authentication
@app.route('/MeDEIsync_DB/user',methods = ['PUT'])
def authentication():
    logger.info('PUT http://localhost:8080/MeDEIsync_DB/user')
    
    payload = flask.request.get_json()
    
    
    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'PUT http://localhost:8080/MeDEIsync_DB/user - payload - {payload}')

    jwt_payload = {}

    if 'username' not in payload or 'password' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'Insira password e username.'}
        conn.close()
        return flask.jsonify(response)
    
    try:
        cur.execute("SELECT cc FROM use WHERE nome = %s AND password = %s",(payload['username'],payload['password']))
        existing_user = cur.fetchone()

        if existing_user:
            # verifica o tipo de utilizador
            funcao =  role(existing_user,cur)

            # encodifica no token o tipo e o cc de quem fez login
            jwt_payload['funcao'] = funcao
            jwt_payload['user_id'] = existing_user[0]
            
            # duracao do login definida em segundos (10 minutos)
            duracao_token = 600
            
            tempo_atual = int(time.time())
            tempo_permitido = tempo_atual + duracao_token

            jwt_payload['duracao_token'] = tempo_permitido

            logger.debug(f'jwt_payload - {jwt_payload}')

            token = jwt.encode(jwt_payload, jwt_key, algorithm = 'HS256')

            response = {'status': StatusCodes['success'], 'results':f"{token}"}
        else:
            response = {'status' : StatusCodes['api_error'],'results': 'Credenciais incorretas'}
            conn.close()
            return flask.jsonify(response)
    except(Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        response = {
            'status': StatusCodes['internal_error'], 'errors': str(error)
        }
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


def role(cc,cur):
    # check if patient
    cur.execute("SELECT use_cc FROM patient WHERE use_cc = %s",cc)
    if cur.fetchone():
        return "patient"
    
    #check if doctor
    cur.execute("SELECT use_cc FROM doctor WHERE use_cc = %s",cc)
    if cur.fetchone():
        return "doctor"
    
    #check if nurse
    cur.execute("SELECT use_cc FROM nurse WHERE use_cc = %s", cc)
    if cur.fetchone():
        return "nurse"
    
    #check if assistant
    cur.execute("SELECT use_cc FROM assistant WHERE use_cc = %s",cc)
    if cur.fetchone():
        return "assistant"


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')