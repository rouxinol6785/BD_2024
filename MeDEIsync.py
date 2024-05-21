import flask
import logging
import psycopg2
import jwt
import random


app = flask.Flask(__name__)


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
        database='MeDEIsync_DB'
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


@app.route('/MeDEIsync_DB/user/registration/patient', methods =['POST'])
def registration():

    logger.info('POST /MeDEIsync_DB/user/registration')
    
    payload = flask.request_get_json()

    conn = db_connection()
    cur = conn.cursor()
    print("helo")

    logger.debug('POST /MeDEIsync_DB/user/registration - payload: {payload}')


    if 'nome' not in payload or 'idade' not in payload  or 'medical_record' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = str(random.randint(0,30))

    statement = 'INSERT INTO patient (id,nome,idade,medical_record) VALUES(%s,%s,%s,%s)'

    values = (id,payload['nome'],payload['idade'],payload['medical_record'])
    try:
        cur.execute("SELECT nome FROM patient WHERE nome = %s",payload['nome'])
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


    
if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')