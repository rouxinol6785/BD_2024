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

#adicionar ao employee colunas - salário, start date, contract(este fica para informações adicionais)

# register patient
@app.route('/MeDEIsync_DB/user/register/patient', methods =['POST'])
def patient_registration():

    logger.info('POST /MeDEIsync_DB/user/register/patient')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/user/registration/patient - payload: {payload}')


    if 'nome'not in payload or 'email' not in payload or 'password' not in payload or 'data_nascimento' not in payload or 'cc' not in payload  or 'n_utente' not in payload or 'nib' not in payload or 'medical_record' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = random.randint(0,30)

    statement = 'INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    statemnt2 = 'INSERT INTO patient (use_cc, medical_record) VALUES(%s,%s)'

    values = (payload['nome'],payload['email'],payload['password'],payload['data_nascimento'],int(payload['cc']), int(payload['n_utente']), payload['nib'])
    values2 = (int (payload['cc']),payload['medical_record'])
    try:
        cur.execute("SELECT nome FROM use WHERE cc = %s",(payload['cc'],))
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
                'status': StatusCodes['success'], 'results': f"Paciente {payload['nome']} inserido!"
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

# register assistant
@app.route('/MeDEIsync_DB/user/register/assistant', methods =['POST'])
def assistant_registration():

    logger.info('POST /MeDEIsync_DB/user/register/assistant')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/user/registration/assistant - payload: {payload}')


    if 'nome'not in payload or 'email' not in payload or 'password' not in payload or 'data_nascimento' not in payload or 'cc' not in payload  or 'n_utente' not in payload or 'nib' not in payload or 'contract' not in payload or 'field_0' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = random.randint(0,30)

    statement = 'INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    statemnt2 = 'INSERT INTO employee (use_cc, contract) VALUES(%s,%s)'
    statemnt3 = 'INSERT INTO assistant (employee_use_cc, field_0) VALUES(%s,%s)'

    values = (payload['nome'],payload['email'],payload['password'],payload['data_nascimento'],int(payload['cc']), int(payload['n_utente']), payload['nib'])
    values2 = (int (payload['cc']),payload['contract'])
    values3 = (int (payload['cc']),int(payload['field_0']))
    try:
        cur.execute("SELECT nome FROM use WHERE cc = %s",(payload['cc'],))
        existing_user = cur.fetchone()
        if existing_user:
            response ={
                'status' : StatusCodes['api_error'], 'results': 'Assistente já está na base de dados'}
            conn.close()
            return flask.jsonify(response)
        else:
            #isto sempre no início das transações, se der merda a meio podemos fazer rollback e volta a como estava aqui
            cur.execute("BEGIN TRANSACTION")
            cur.execute(statement,values)
            cur.execute(statemnt2,values2)
            cur.execute(statemnt3,values3)
            conn.commit()
            response = {
                'status': StatusCodes['success'], 'results': f"Assistente {payload['nome']} inserido!"
            }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/registration/assistant - error: {error}')
        response = {
            'status': StatusCodes['internal_error'], 'errors': str(error)
        }
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)



# register nurse
@app.route('/MeDEIsync_DB/user/register/nurse', methods =['POST'])
def nurse_registration():

    logger.info('POST /MeDEIsync_DB/user/register/nurse')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/user/registration/nurse - payload: {payload}')


    if 'nome'not in payload or 'email' not in payload or 'password' not in payload or 'data_nascimento' not in payload or 'cc' not in payload  or 'n_utente' not in payload or 'nib' not in payload or 'contract' not in payload or 'internal_hierarchy' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = random.randint(0,30)

    statement = 'INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    statemnt2 = 'INSERT INTO employee (use_cc, contract) VALUES(%s,%s)'
    statemnt3 = 'INSERT INTO nurse (employee_use_cc, internal_hierarchy) VALUES(%s,%s)'

    values = (payload['nome'],payload['email'],payload['password'],payload['data_nascimento'],int(payload['cc']), int(payload['n_utente']), payload['nib'])
    values2 = (int (payload['cc']),payload['contract'])
    values3 = (int (payload['cc']),payload['internal_hierarchy'])
    try:
        cur.execute("SELECT nome FROM use WHERE cc = %s",(payload['cc'],))
        existing_user = cur.fetchone()
        if existing_user:
            response ={
                'status' : StatusCodes['api_error'], 'results': 'Enfermeir@ já está na base de dados'}
            conn.close()
            return flask.jsonify(response)
        else:
            #isto sempre no início das transações, se der merda a meio podemos fazer rollback e volta a como estava aqui
            cur.execute("BEGIN TRANSACTION")
            cur.execute(statement,values)
            cur.execute(statemnt2,values2)
            cur.execute(statemnt3,values3)
            conn.commit()
            response = {
                'status': StatusCodes['success'], 'results': f"Enfermeir@ {payload['nome']} inserid@!"
            }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/registration/nurse - error: {error}')
        response = {
            'status': StatusCodes['internal_error'], 'errors': str(error)
        }
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)




# register doctor
@app.route('/MeDEIsync_DB/user/register/doctor', methods =['POST'])
def doctor_registration():

    logger.info('POST /MeDEIsync_DB/user/register/doctor')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/user/registration/doctor - payload: {payload}')


    if 'nome'not in payload or 'email' not in payload or 'password' not in payload or 'data_nascimento' not in payload or 'cc' not in payload  or 'n_utente' not in payload or 'nib' not in payload or 'contract' not in payload or 'medical_license' not in payload or 'main_specialization' not in payload:
        response = {
            'status': StatusCodes['api_error'], 'results':'Missing required fields'
        }
        conn.close()
        return flask.jsonify(response)
    
    #para fazer o ID o melhor é fazer o autoincrement da base de dados
    id = random.randint(0,30)

    statement = 'INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    statemnt2 = 'INSERT INTO employee (use_cc, contract) VALUES(%s,%s)'
    statemnt3 = 'INSERT INTO doctor (employee_use_cc, medical_license, main_specialization) VALUES(%s,%s,%s)'

    values = (payload['nome'],payload['email'],payload['password'],payload['data_nascimento'],int(payload['cc']), int(payload['n_utente']), payload['nib'])
    values2 = (int (payload['cc']),payload['contract'])
    values3 = (int (payload['cc']),payload['medical_license'], payload['main_specialization'])
    try:
        cur.execute("SELECT nome FROM use WHERE cc = %s",(payload['cc'],))
        existing_user = cur.fetchone()
        if existing_user:
            response ={
                'status' : StatusCodes['api_error'], 'results': 'Médic@ já está na base de dados'}
            conn.close()
            return flask.jsonify(response)
        else:
            #isto sempre no início das transações, se der merda a meio podemos fazer rollback e volta a como estava aqui
            cur.execute("BEGIN TRANSACTION")
            cur.execute(statement,values)
            cur.execute(statemnt2,values2)
            cur.execute(statemnt3,values3)
            conn.commit()
            response = {
                'status': StatusCodes['success'], 'results': f"Medic@ {payload['nome']} inserid@!"
            }
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/registration/doctor - error: {error}')
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


#Schedule Appointment

###### IMPORTANTE -> para testar este endpoint é necessário adicionar uma nova bill devido a constraints, ou então implementar o que está em baixo.
'''
Falta criar o trigger para a bill
bill pede o nif (do paciente)
'''
@app.route('/MeDEIsync_DB/appointment', methods= ['POST'])
def schedule_appointment():
    logger.info('POST /MeDEIsync_DB/appointment')
    payload = flask.request.get_json()

    logger.debug(f'POST /MeDEIsync_DB/appointment - payload: {payload}')

    #appointment_nurse opcional
    if 'doctor_cc' not in payload or 'date' not in payload or 'type' not in payload or 'price' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'payload should be have: doctor_cc - date - type - price'}
        return flask.jsonify(response)
    

    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])
    
    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)
    

    if decode['funcao'] != 'patient':
        response = {'status': StatusCodes['api_error'], 'results': 'Must be a patient to use this endpoint.'}
        return flask.jsonify(response)
    
   
    statement = 'INSERT INTO appointment (ap_date,patient_use_cc,doctor_employee_use_cc,bill_id) VALUES (%s,%s,%s,%s)'
    values = (payload['date'],int(decode['user_id']),int(payload['doctor_cc']),1)
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT (employee_use_cc) FROM doctor WHERE employee_use_cc = %s',(payload['doctor_cc'],))
        doc = cur.fetchone()
        if doc:
            pass
        else:
            response = {'status': StatusCodes['api_error'], 'results': 'The doctor_cc you inserted does not exist.'}
            return flask.jsonify(response)
        cur.execute("BEGIN TRANSACTION")
        cur.execute(statement,values)
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': 'appointment added!'}
    
    except(Exception,psycopg2.DatabaseError)as error:
        logger.error(f'POST /MeDEIsync_DB/appointment - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return flask.jsonify(response)


# feito
#see appointments
@app.route('/MeDEIsync_DB/appointments/<patient_id>', methods = ['GET'])
def see_appointments(patient_id):
    logger.info('GET MeDEIsync_DB/appointments/<patient_user_id>')
    logger.debug(f'patient_cc: {patient_id}')

  

    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])
    
  
    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)
    
    conn = db_connection()
    cur = conn.cursor()
    
    if decode['funcao'] == 'patient' or decode['funcao'] == 'assistant':
        try:
            cur.execute('''
                SELECT u.nome, a.ap_date 
                FROM appointment AS a
                LEFT JOIN use AS u 
                ON a.doctor_employee_use_cc = u.cc 
                WHERE a.patient_use_cc = %s
            ''', (patient_id,))            
            rows = cur.fetchall()
            if rows:
                response = {'status':StatusCodes['success'], 'results': rows}
            else:
                response = {'status':StatusCodes['success'], 'results': 'No appointments for this user'}
                
        except(Exception, psycopg2.DatabaseError) as error:
            logger.error(f'GET /MeDEIsync_DB/appointments - error: {error}')
            response = {'status': StatusCodes['internal_error'],'error':str(error)}
        finally:
            if conn is not None:
                conn.close() 
    else:
        response = {'status':StatusCodes['api_error'],'results': 'user not allowed to perform this action.'}
    return flask.jsonify(response)

#schedule surgery, hospitalization not provided
# FALTA bill update/create -> triggers
# alter results -> its a schedule not a log
@app.route('/MeDEIsync_DB/surgery', methods = ['POST'])
def schedule_surgery_no_hospitalization():
    logger.info('POST /MeDEIsync_DB/surgery')

    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])

    
    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)

    if decode['funcao'] != 'assistant':
        response = {'status': StatusCodes['api_error'],'results': 'Only assistants allowed to schedule surgeries.'}
        return flask.jsonify(response)
    
    payload = flask.request.get_json()
    logger.debug(f'POST /MeDEIsync_DB/surgery - payload:{payload}')

    if 'patient_id' not in payload or 'doctor' not in payload or  'nurses' not in payload or 'date' not in payload or 'duration' not in payload or 'result' not in payload:
        response = {'status': StatusCodes['api_error'], 'results': 'payload should be: patient_id - doctor - nurses - date.'}
        return flask.jsonify(response)

    hospitalization = 'INSERT INTO hospitalization (data_inic, bill_id, assistant_employee_use_cc, nurse_employee_use_cc, patient_use_cc) VALUES (%s,%s,%s,%s,%s) RETURNING id'
    hosp_values = (payload['date'],3,decode['user_id'], payload['nurses'][0][0],payload['patient_id'])

    surgery = 'INSERT INTO surgery(surgery_date, duration, results, hospitalization_id) VALUES (%s,%s,%s,%s) RETURNING id'

    surgery_nurses = 'INSERT INTO surgery_nurse (role,nurse_employee_use_cc, surgery_id) VALUES(%s,%s,%s)'

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN TRANSACTION")
        cur.execute(hospitalization,hosp_values)
        hosp_id = cur.fetchone()
        hosp_id = hosp_id[0]

        surg_values = (payload['date'],int(payload['duration']),payload['result'],hosp_id)
        cur.execute(surgery,surg_values)
        surg_id = cur.fetchone()
        surg_id = surg_id[0]

        for row in payload['nurses']:
            nurses_values = (row[1],row[0],surg_id)
            cur.execute(surgery_nurses,nurses_values)
        conn.commit()

        response = {'status': StatusCodes['success'],
                    'results': f'"hospitalization_id": {hosp_id}, "surgery_id":{surg_id}, "patient_id": {payload['patient_id']}, "date": {payload['date']}'}
    except (Exception,psycopg2.DatabaseError) as error:
        logger.error(f'')
        response = {'status': StatusCodes['internal_error'],
                    'error': str(error)}
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


#execute payment
@app.route('/MeDEIsync_DB/bills/<bill_id>', methods =  ['POST'])
def payment(bill_id):
    logger.info('POST /MeDEIsync_DB/bills')

    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])
    
  
    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)
    
    if decode['funcao'] != 'patient':
        response = {'status':StatusCodes['api_error'], "error":'Only patients can pay their own bills'}


def role(cc,cur):
    # check if patient
    cur.execute("SELECT use_cc FROM patient WHERE use_cc = %s",cc)
    if cur.fetchone():
        return "patient"
    
    #check if doctor
    cur.execute("SELECT employee_use_cc FROM doctor WHERE employee_use_cc = %s",cc)
    if cur.fetchone():
        return "doctor"
    
    #check if nurse
    cur.execute("SELECT employee_use_cc FROM nurse WHERE employee_use_cc = %s", cc)
    if cur.fetchone():
        return "nurse"
    
    #check if assistant
    cur.execute("SELECT employee_use_cc FROM assistant WHERE employee_use_cc = %s",cc)
    if cur.fetchone():
        return "assistant"
    
def time_up(token):
    t = int(time.time())
    if t > token:
        response = {'status':StatusCodes['api_error'],'results': 'sessão expirada, por favor inicie sessão novamente.'}
        return response
    else:
        return 0


def temporary_insert():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)",('carlos', 'carlos@gmail.com','pass_do_carlos','2003-01-11',123456789,1298746,"PT89729467914"))
    cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (123456789,'yolo'))
    cur.execute("INSERT INTO doctor(employee_use_cc,medical_license,main_specialization) VALUES(%s,%s,%s)",(123456789,'uc','neuroscience'))

    
    cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)",('fatima', 'fatima@gmail.com','pass_da?fatima','2000-04-11',987654321,412354235,"PT0987125769"))
    cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (987654321,'yolo'))
    cur.execute("INSERT INTO nurse(employee_use_cc,internal_hierarchy) VALUES(%s,%s)",(987654321,'chief_nurse'))


    
    cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)",('endre', 'andre@gmail.com','pass_do?andre','2004-03-10',112233445,9821747,"PT098791256721"))
    cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (112233445,'yolo'))
    cur.execute("INSERT INTO assistant(employee_use_cc,field_0) VALUES(%s,%s)",(112233445,'chief_assistant'))

    
    cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES(%s,%s,%s,%s,%s,%s,%s)",('jesus', 'jesus@gmail.com','pass_do?jesus','1950-10-20',887766554,9864218,"PT09832176812345"))
    cur.execute("INSERT INTO patient(use_cc,medical_record) VALUES(%s,%s)",(887766554,'yolo'))
    conn.commit()
    conn.close()
    return 1

def add_bill(user_id,bill_ammount)
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO bill (nif,ammount,patient_use_cc) VALUES(%s,%s,%s)"(bill_ammount,bill_ammount,user_id))
    conn.commit()
    conn.close()
    return 1

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')