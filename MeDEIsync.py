import logging
import random
import time
import psycopg2
import jwt
import flask



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
    temporary_insert()
    #add_bill(4567,2)
    return"""
    Bem-vindo!<br/>
"""

#adicionar ao employee colunas - salário, start date, contract(este fica para informações adicionais)

# register patient
@app.route('/MeDEIsync_DB/register/patient', methods =['POST'])
def patient_registration():

    logger.info('POST /MeDEIsync_DB/register/patient')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/registration/patient - payload: {payload}')


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
                'status': StatusCodes['success'], 'results': f"Paciente {payload['nome']} inserido! cc - {payload['cc']}"
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
@app.route('/MeDEIsync_DB/register/assistant', methods =['POST'])
def assistant_registration():

    logger.info('POST /MeDEIsync_DB/register/assistant')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/registration/assistant - payload: {payload}')


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
                'status': StatusCodes['success'], 'results': f"Assistente {payload['nome']} inserido! cc - {payload['cc']}"
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
@app.route('/MeDEIsync_DB/register/nurse', methods =['POST'])
def nurse_registration():

    logger.info('POST /MeDEIsync_DB/register/nurse')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/registration/nurse - payload: {payload}')


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
                'status': StatusCodes['success'], 'results': f"Enfermeir@ {payload['nome']} inserid@! cc - {payload['cc']}"
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
@app.route('/MeDEIsync_DB/register/doctor', methods =['POST'])
def doctor_registration():

    logger.info('POST /MeDEIsync_DB/register/doctor')
    
    payload = flask.request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.debug(f'POST /MeDEIsync_DB/use/registration/doctor - payload: {payload}')


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
                'status': StatusCodes['success'], 'results': f"Medic@ {payload['nome']} inserid@! cc - {payload['cc']}"
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
    if 'doctor_cc' not in payload or 'date' not in payload or 'type' not in payload:
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
    
   
    statement = 'INSERT INTO appointment (ap_date,patient_use_cc,doctor_employee_use_cc) VALUES (%s,%s,%s) RETURNING id'
    values = (payload['date'],int(decode['user_id']),int(payload['doctor_cc']))
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
        app_id = cur.fetchone()
        conn.commit()
        response = {'status': StatusCodes['success'], 'results': f'appointment added! id - {app_id[0]}'}
    
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

#nao sei se está bem
#get prescriptions
@app.route('/MeDEIsync_DB/prescriptions/<person_id>', methods=['GET'])
def get_prescriptions(person_id):
    logger.info(f'GET /MeDEIsync_DB/prescriptions/{person_id}')
    logger.debug(f'person_id: {person_id}')

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        return flask.jsonify({'status': 'error', 'message': 'Authorization header is missing'}), 401

    try:
        jwt_token = jwt_token.split('Bearer ')[1]  # Remove extra characters
        decode = jwt.decode(jwt_token, jwt_key, algorithms=['HS256'])
    except Exception as e:
        logger.error(f'JWT decode error: {e}')
        return flask.jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response), 401

    conn = db_connection()
    cur = conn.cursor()

    if decode['funcao'] == 'patient' and decode['cc'] == person_id or decode['funcao'] == 'employee':
        try:
            cur.execute('''
                SELECT p.prescription_id, p.medication, p.dosage, p.start_date, p.end_date, d.name AS doctor_name 
                FROM prescriptions AS p
                LEFT JOIN doctors AS d ON p.doctor_id = d.doctor_id 
                WHERE p.patient_id = %s
            ''', (person_id,))
            rows = cur.fetchall()
            if rows:
                response = {'status': 'success', 'results': rows}
            else:
                response = {'status': 'success', 'results': 'No prescriptions for this user'}
                
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'GET /MeDEIsync_DB/prescriptions - error: {error}')
            response = {'status': 'internal_error', 'error': str(error)}
        finally:
            if conn is not None:
                conn.close()
    else:
        response = {'status': 'api_error', 'message': 'User not allowed to perform this action.'}
        
    return flask.jsonify(response)


#get top3
@app.route('/MeDEIsync_DB/top3', methods=['GET'])
def get_top3():
    logger.info(f'GET /MeDEIsync_DB/top3')

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        return flask.jsonify({'status': 'error', 'message': 'Authorization header is missing'}), 401

    try:
        jwt_token = jwt_token.split('Bearer ')[1]  # Remove extra characters
        decode = jwt.decode(jwt_token, jwt_key, algorithms=['HS256'])
    except Exception as e:
        logger.error(f'JWT decode error: {e}')
        return flask.jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response), 401

    conn = db_connection()
    cur = conn.cursor()

    if decode['funcao'] == 'assistant':
        try:
            cur.execute('''
                SELECT 
                    u.cc,
                    u.nome,
                    SUM(b.ammount) AS total_spent,
                    a.id,
                    a.ap_date,
                    h.id,
                    h.data_inic
                FROM 
                    use u
                JOIN 
                    bill b ON u.cc = b.patient_use_cc
                LEFT JOIN
                    appointment a ON b.id = a.bill_id
                LEFT JOIN
                    hospitalization_bill hb ON b.id = hb.bill_id
                LEFT JOIN
                    hospitalization as h ON hb.hospitalization_id = h.id
                GROUP BY 
                    u.cc,u.nome,a.id,h.id
                ORDER BY 
                    total_spent DESC
                LIMIT 3;
            ''')
            rows = cur.fetchall()
            if rows:
                response = {'status': 'success', 'results': rows}
            else:
                response = {'status': 'success', 'results': 'No prescriptions for this user'}
                
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'GET /MeDEIsync_DB/top3 - error: {error}')
            response = {'status': 'internal_error', 'error': str(error)}
        finally:
            if conn is not None:
                conn.close()
    else:
        response = {'status': 'api_error', 'message': 'User not allowed to perform this action.'}
        
    return flask.jsonify(response)





#daily summary
@app.route('/MeDEIsync_DB/daily/<data_dia>', methods=['GET'])
def daily_summary(data_dia):
    logger.info(f'GET /MeDEIsync_DB/daily/<data_dia>')
    logger.debug(f'person_id: {data_dia}')

    jwt_token = flask.request.headers.get('Authorization')
    if not jwt_token:
        return flask.jsonify({'status': 'error', 'message': 'Authorization header is missing'}), 401

    try:
        jwt_token = jwt_token.split('Bearer ')[1]  # Remove extra characters
        decode = jwt.decode(jwt_token, jwt_key, algorithms=['HS256'])
    except Exception as e:
        logger.error(f'JWT decode error: {e}')
        return flask.jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response), 401

    conn = db_connection()
    cur = conn.cursor()

    if decode['funcao'] == 'assistant':
        try:
            cur.execute('''
                    SELECT
                        (SELECT COUNT(*) FROM surgery WHERE surgery_date = %s),
                        (SELECT SUM(paid_amomunt) FROM payment WHERE pay_date = %s),
                        (SELECT COUNT(*) FROM surgery WHERE surgery_date = %s)
            ''',(data_dia,data_dia,data_dia))
            rows = cur.fetchone()
            if rows:
                response = {'status': 'success', 'results': f'surgeries - {rows[0]}, ammount spent - {rows[1]}, prescriptions - {rows[0]}'}
            else:
                response = {'status': 'success', 'results': 'No prescriptions for this user'}
                
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f'GET /MeDEIsync_DB/daily/<data_dia> - error: {error}')
            response = {'status': 'internal_error', 'error': str(error)}
        finally:
            if conn is not None:
                conn.close()
    else:
        response = {'status': 'api_error', 'message': 'User not allowed to perform this action.'}
        
    return flask.jsonify(response)



#schedule surgery, hospitalization not provided
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

    hospitalization = 'INSERT INTO hospitalization (data_inic, assistant_employee_use_cc, nurse_employee_use_cc, patient_use_cc) VALUES (%s,%s,%s,%s) RETURNING id'
    hosp_values = (payload['date'],decode['user_id'], payload['nurses'][0][0],int(payload['patient_id']))

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
                    'results': f'"hospitalization_id": {hosp_id}, "surgery_id":{surg_id}, "doctor_id": {payload["doctor_id"]}, "patient_id": {payload["patient_id"]}, "date": {payload["date"]}'}
    except (Exception,psycopg2.DatabaseError) as error:
        logger.error(f'')
        response = {'status': StatusCodes['internal_error'],
                    'error': str(error)}
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)

# schedule surgery with hospitalization
@app.route('/MeDEIsync_DB/surgery/<h_id>', methods = ['POST'])
def schedule_surgery(h_id):
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
    surgery = 'INSERT INTO surgery(surgery_date, duration, results, hospitalization_id) VALUES (%s,%s,%s,%s) RETURNING id'

    surgery_nurses = 'INSERT INTO surgery_nurse (role,nurse_employee_use_cc, surgery_id) VALUES(%s,%s,%s)'

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN TRANSACTION")
        cur.execute('SELECT id FROM hospitalization WHERE id = %s',(h_id,))
        i = cur.fetchone()
        if i:
            pass
        else:
            response = {'status': StatusCodes['api_error'], 'error': 'hospitalization id is not correct.'}
            conn.close()
            return flask.jsonify(response)
        surg_values = (payload['date'],int(payload['duration']),payload['result'],h_id)
        cur.execute(surgery,surg_values)
        surg_id = cur.fetchone()
        surg_id = surg_id[0]

        for row in payload['nurses']:
            nurses_values = (row[1],row[0],surg_id)
            cur.execute(surgery_nurses,nurses_values)
        conn.commit()

        response = {'status': StatusCodes['success'],
                    'results': f'"hospitalization_id": {h_id}, "surgery_id":{surg_id}, "patient_id": {payload["patient_id"]}, "date": {payload["date"]}'}
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

    payload = flask.request.get_json()

    if 'date' not in payload or 'ammount' not in payload or 'method' not in payload:
        response = {'status': StatusCodes['api_error'], 'error': 'payload should be: date - ammount - method.'}
    pay_ammmount = int(payload['ammount'])

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN TRANSACTION")
        cur.execute("SELECT (ammount,patient_use_cc) FROM bill WHERE id = %s",(bill_id))
        query = cur.fetchone()
        query = query[0].split('(')
        query = query[1].split(')')
        query = query[0].split(',')
        if query:
            if int(query[1]) == decode['user_id']:
                
                if pay_ammmount >= int(query[0]):
                    new_ammount = pay_ammmount - int(query[0])

                    values = (payload['date'],new_ammount,payload['method'],decode['user_id'],bill_id)
                    cur.execute("UPDATE public.bill SET ammount = 0, status = 'paid' WHERE id = %s",(bill_id,))
                    cur.execute("INSERT INTO payment(pay_date,paid_amount,payment_method,patient_use_cc,bill_id) VALUES (%s,%s,%s,%s,%s)", values) 
                    response = {'status':StatusCodes['success'], 'results': 'bill paid!'}
                else:
                    new_ammount = int(query[0]) - pay_ammmount
                    values = (payload['date'],new_ammount,payload['method'],decode['user_id'],bill_id)

                    cur.execute("UPDATE bill SET ammount = %s WHERE id = %s",(new_ammount,bill_id))
                    cur.execute("INSERT INTO payment(pay_date,paid_ammount,payment_method,patient_use_cc,bill_id) VALUES(%s,%s,%s,%s,%s)",(payload['date'],pay_ammmount,payload['method'],decode['user_id'],bill_id)) ###
                    response = {'status':StatusCodes['success'], 'results': f'bill deducted, ammount left - {new_ammount}'}

            else:
                response = {'status': StatusCodes['api_error'], 'error': 'Error accessing bill'}
        else:
            response = {'status': StatusCodes['api_error'], 'error': 'Only the owner patient can pay his/her bill.'}
            conn.close()
            return flask.jsonify(response)
    except (Exception,psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/bills - error: {error}')
        response = {'status':StatusCodes['internal_error'], 'errors': str(error)}
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


#add prescription
@app.route('/MeDEIsync_DB/prescription', methods = ['POST'])
def add_prescription():
    logger.info('POST /MeDEIsync_DB/prescription')
    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])

    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)
    
    if decode['funcao'] != 'doctor':
        response = {'status':StatusCodes['api_error'], "error":'Only doctors can add prescriptions'}
        return flask.jsonify(response)

    payload = flask.request.get_json()
    if 'type' not in payload or 'event_id' not in payload or 'validity' not in payload or 'medicines' not in payload or 'patient_id' not in payload:
        response = {'status': StatusCodes['api_error'], 'error': 'payload should contain: type - event_id - validity - medicines {"medcine": "medicine_name","posology_dose": value,"posology_frequency": value}'}
        return flask.jsonify(response)
    logger.debug(f'POST /MeDEIsync_DB/prescription - error: {payload}')

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN TRANSACTION")
        cur.execute('SELECT medical_record FROM patient where use_cc = %s', (int(payload['patient_id']),))
        medical_record = cur.fetchone()
        if medical_record:
            pass
        else:
            response = {'status':StatusCodes['api_error'], 'error': 'Couldnt find patient'}
            conn.close()
            return flask.jsonify(response)
        
        if payload['type'] == 'hospitalization':
            cur.execute('SELECT id FROM hospitalization WHERE id = %s',(payload['event_id'],))
            hosp = cur.fetchone()
            if hosp:
                pass
            else:
                response = {'status':StatusCodes['api_error'], 'error': 'Error in event_id'}
                conn.close()
                return flask.jsonify(response)
            
            cur.execute("INSERT INTO prescription (doctor_employee_use_cc,patient_use_cc,validity) VALUES(%s,%s,%s) RETURNING id",(decode['user_id'],payload['patient_id'],payload['validity']))
            presc_id = cur.fetchone()
            if presc_id:
                for row in payload['medicines']:
                    cur.execute('SELECT id FROM medication WHERE name = %s',(row['medicine'],))
                    med_id = cur.fetchone()
                    
                    if med_id:
                        cur.execute('INSERT INTO prescription_medication (dosage,medication_id,frequency,prescription_id) VALUES (%s,%s,%s,%s)',(row['dosage'],med_id[0],row['frequency'],presc_id[0]))
                    else:
                        response = {'status':StatusCodes['api_error'],'error': f"couldn't find medicine {row['medicine']}"}
                        conn.rollback()
                        conn.close()
                        return flask.jsonify(response)
            else:
                response = {'status':StatusCodes['api_error'],'error': f"Error adding prescription."}
                conn.rollback()
                conn.close()
                return flask.jsonify(response)
            
            cur.execute('INSERT INTO hospitalization_prescription (hospitalization_id,prescription_id) VALUES(%s,%s)', (hosp[0],presc_id[0]))
            conn.commit()
            response = {'status':StatusCodes['success'], 'success': f'prescription added!!  prescription_id - {presc_id[0] }'}
        
        elif payload['type'] == 'appointment':
            cur.execute('SELECT id from appointment WHERE id = %s',(payload['event_id'],))
            appo = cur.fetchone()
            if cur:
                pass
            else:
                response = {'status':StatusCodes['api_error'], 'error': 'Error in event_id'}
                conn.close()
                return flask.jsonify(response)
            
            cur.execute("INSERT INTO prescription (doctor_employee_use_cc,patient_use_cc,validity) VALUES(%s,%s,%s) RETURNING id",(decode['user_id'],payload['patient_id'],payload['validity']))
            presc_id = cur.fetchone()
            
            for row in payload['medicines']:
                cur.execute('SELECT id FROM medication WHERE name = %s',(row['medicine'],))
                med_id = cur.fetchone()
                
                if med_id:
                    cur.execute('INSERT INTO prescription_medication (dosage,medication_id,frequency,prescription_id) VALUES (%s,%s,%s,%s)',(row['dosage'],med_id[0],row['frequency'],presc_id[0]))
                
                else:
                    response = {'status':StatusCodes['api_error'],'error': f"couldn't find medicine {row['medicine']}"}
                    conn.rollback()
                    conn.close()
                    return flask.jsonify(response)
            cur.execute('INSERT INTO prescription_appointment (appointment_id,prescription_id), VALUES(%d,%d)',(appo[0],presc_id[0]))
            conn.commit()
            response = {'status':StatusCodes['success'], 'success': f'prescription added!!  prescription_id - {presc_id[0]}'}

        else:
            response = {'status':StatusCodes['api_error'], 'error': 'type not valid.'}
            conn.close()
            return flask.jsonify(response)

    except(Exception,psycopg2.DatabaseError) as error:
        logger.error(f'POST /MeDEIsync_DB/prescription - error:{payload}')
        response = {'status': StatusCodes['internal_error'],'errors': str(error)}
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return flask.jsonify(response)


#Generate monthly report
@app.route('/MeDEIsync_DB/report',methods = ['GET'])
def report():
    logger.info('MeDEIsync_DB/report')
    jwt_token = flask.request.headers.get('Authorization')
    jwt_token = jwt_token.split('Bearer ')[1]   #remove extra characters
    decode = jwt.decode(jwt_token,jwt_key,algorithms = ['HS256'])

    if time_up(decode['duracao_token']) != 0:
        response = time_up(decode['duracao_token'])
        return flask.jsonify(response)
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''WITH surgery_counts AS (
            SELECT
                ds.doctor_employee_use_cc,
                TO_CHAR(s.surgery_date, 'YYYY-MM') AS month,
                COUNT(*) AS surgeries_count,
                ROW_NUMBER() OVER (PARTITION BY TO_CHAR(s.surgery_date, 'YYYY-MM') ORDER BY COUNT(*) DESC) AS rn
            FROM surgery s
                            
            RIGHT JOIN doctor_surgery ds ON s.id = ds.surgery_id
                            
            WHERE s.surgery_date >= (CURRENT_DATE - INTERVAL '12 months')
            GROUP BY ds.doctor_employee_use_cc,
                TO_CHAR(s.surgery_date, 'YYYY-MM')
                )
                            
            SELECT
                doctor_employee_use_cc,
                month,
                surgeries_count
            FROM surgery_counts
            WHERE rn = 1
            ORDER BY month;''')
        t = cur.fetchall()
        response = {'status': StatusCodes['success'], 'success': f'results {t}'}
    except(Exception,psycopg2.DatabaseError) as error:
        logger.debug(f'/MeDEIsync_DB/report error - {error}')
        response = {'status':StatusCodes['internal_error'],'error': str(error)}
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
    
    try:
        #info pacientes
        pacientes_nome          =["paciente1"               ,"paciente2"                ,"paciente3"                ,"paciente4"                ,"paciente5"                ]
        pacientes_id            =[101                       ,102                        ,103                        ,104                        ,105                   ]
        pacientes_email         =["paciente1@gmail.com"     ,"paciente2@gmail.com"      ,"paciente3@gmail.com"      ,"paciente4@gmail.com"      ,"paciente5@gmail.com"      ]
        pacientes_password      =["password1"               ,"password2"                ,"password3"                ,"password4"                ,"password5"                ]
        pacientes_data          =["1995-1-5"                ,"1996-2-10"                ,"1997-3-15"                ,"1998-4-20"                ,"1999-5-25"                ]
        pacientes_n_utente      =[11111111                  ,11111112                   ,11111113                   ,11111114                   ,11111115                   ]
        pacientes_nib           =["PT5010000000001"         ,"PT5010000000002"          ,"PT5010000000003"          ,"PT5010000000004"          ,"PT5010000000005"          ]
        pacientes_medical_rec   =["medical_rec1"            ,"medical_rec1"             ,"medical_rec1"             ,"medical_rec1"             ,"medical_rec1"             ]


        #info medicos
        medicos_nome            =["medico1"                 ,"medico2"                  ,"medico3"                  ,"medico4"                  ,"medico5"                  ]
        medicos_id              =[201                       ,202                        ,203                        ,204                        ,205                   ]
        medicos_email           =["medico1@gmail.com"       ,"medico2@gmail.com"        ,"medico3@gmail.com"        ,"medico4@gmail.com"        ,"medico5@gmail.com"        ]
        medicos_password        =["password1"               ,"password2"                ,"password3"                ,"password4"                ,"password5"                ]
        medicos_data            =["1995-1-5"                ,"1996-2-10"                ,"1997-3-15"                ,"1998-4-20"                ,"1999-5-25"                ]
        medicos_n_utente        =[22222221                  ,22222222                   ,22222223                   ,22222224                   ,22222225                   ]
        medicos_nib             =["PT5020000000001"         ,"PT5020000000002"          ,"PT5020000000003"          ,"PT5020000000004"          ,"PT5020000000005"          ]
        medicos_license         =["universidade de coimbra" ,"universidade de lisboa"   ,"universidade do porto"    ,"universidade do minho"    ,"universidade do algarve"  ]
        medicos_specialization  =["genecologia"             ,"ortopedia"                ,"cardiologia"              ,"neurologia"               ,"cirurgia"                 ]
        

        #info enfermeiros
        enfermeiros_nome        =["enfermeiro1"             ,"enfermeiro2"              ,"enfermeiro3"              ,"enfermeiro4"              ,"enfermeiro5"              ]
        enfermeiros_id          =[301                       ,302                        ,303                        ,304                        ,305                   ]
        enfermeiros_email       =["enfermeiro1@gmail.com"   ,"enfermeiro2@gmail.com"    ,"enfermeiro3@gmail.com"    ,"enfermeiro4@gmail.com"    ,"enfermeiro5@gmail.com"    ]
        enfermeiros_password    =["password1"               ,"password2"                ,"password3"                ,"password4"                ,"password5"                ]
        enfermeiros_data        =["1995-1-5"                ,"1996-2-10"                ,"1997-3-15"                ,"1998-4-20"                ,"1999-5-25"                ]      
        enfermeiros_n_utente    =[33333331                  ,33333332                   ,33333333                   ,33333334                   ,33333335                   ]
        enfermeiros_nib         =["PT5030000000001"         ,"PT5030000000002"          ,"PT5030000000003"          ,"PT5030000000004"          ,"PT5030000000005"          ]
        enfermeiros_hierarquia  =["chefe"                   ,"auxiliar"                 ,"assistente"               ,"supervisor"               ,"chefe de unidade"         ]


        #info assistentes
        assistentes_nome        =["assistente1"             ,"assistente2"              ,"assistente3"              ,"assistente4"              ,"assistente5"              ]
        assistentes_id          =[401                       ,402                        ,403                        ,404                        ,405                   ]
        assistentes_email       =["assistente1@gmail.com"   ,"assistente2@gmail.com"    ,"assistente3@gmail.com"    ,"assistente4@gmail.com"    ,"assistente5@gmail.com"    ]
        assistentes_password    =["password1"               ,"password2"                ,"password3"                ,"password4"                ,"password5"                ]
        assistentes_data        =["1995-1-5"                ,"1996-2-10"                ,"1997-3-15"                ,"1998-4-20"                ,"1999-5-25"                ]
        assistentes_n_utente    =[44444441                  ,44444442                   ,44444443                   ,44444444                   ,44444445                   ]
        assistentes_nib         =["PT5040000000001"         ,"PT5040000000002"          ,"PT5040000000003"          ,"PT5040000000004"          ,"PT5040000000005"          ]
        assistente_field_0      =[1                         ,2                          ,3                          ,4                          ,5] 

        #tempos dos contratos (melhor meter data de fim)
        contratos               =["2 anos"                  ,"3 anos"                   ,"1 ano"                    ,"5 anos"                   ,"3 anos"                   ]

        j = 1
        cur.execute("BEGIN TRANSACTION")
        #insere pacientes
        for i in range(5):
            cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES (%s,%s,%s,%s,%s,%s,%s)",(pacientes_nome[i], pacientes_email[i], pacientes_password[i], pacientes_data[i], pacientes_id[i], pacientes_n_utente[i], pacientes_nib[i]))
            cur.execute("INSERT INTO patient(medical_record,use_cc) VALUES(%s,%s)",(pacientes_medical_rec[i], pacientes_id[i]))
            j=j+1

        #insere medicos
        for i in range(5):
            cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES (%s,%s,%s,%s,%s,%s,%s)",(medicos_nome[i], medicos_email[i], medicos_password[i], medicos_data[i], medicos_id[i], medicos_n_utente[i], medicos_nib[i]))
            cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (medicos_id[i], contratos[i]))
            cur.execute("INSERT INTO doctor(employee_use_cc,medical_license,main_specialization) VALUES(%s,%s,%s)",(medicos_id[i], medicos_license[i], medicos_specialization[i]))
            j=j+1

        #insere enfermeiros
        for i in range(5):
            cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES (%s,%s,%s,%s,%s,%s,%s)",(enfermeiros_nome[i], enfermeiros_email[i], enfermeiros_password[i], enfermeiros_data[i], enfermeiros_id[i], enfermeiros_n_utente[i], enfermeiros_nib[i]))
            cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (enfermeiros_id[i], contratos[i]))
            cur.execute("INSERT INTO nurse(employee_use_cc,internal_hierarchy) VALUES(%s,%s)",(enfermeiros_id[i], enfermeiros_hierarquia[i]))
            j=j+1

        #insere assistentes
        for i in range(5):
            cur.execute("INSERT INTO use (nome, email, password, data_nascimento, cc, n_utente, nib) VALUES (%s,%s,%s,%s,%s,%s,%s)",(assistentes_nome[i], assistentes_email[i], assistentes_password[i], assistentes_data[i], assistentes_id[i], assistentes_n_utente[i], assistentes_nib[i]))
            cur.execute("INSERT INTO employee (use_cc, contract) VALUES(%s,%s)", (assistentes_id[i], contratos[i]))
            cur.execute("INSERT INTO assistant(employee_use_cc,field_0) VALUES(%s,%s)",(assistentes_id[i], assistente_field_0[i]))
            j=j+1  


        #insere side effects
        side_effects    =["side_effect1"    ,"side_effect1" ,"side_effect1" ,"side_effect1" ,"side_effect1"]
        side_effect_ids =[]
        for i in range(5):
            cur.execute("INSERT INTO side_effect (description) VALUES (%s) RETURNING id",(side_effects[i],))
            id = cur.fetchone()[0]
            side_effect_ids.append(id)
        j=j+1
        #insere medicamentos
        medication  =["medication1","medication2","medication3","medication4","medication5"]
        medication_ids =[]
        for i in range(5):
            cur.execute("INSERT INTO medication (name) VALUES (%s) RETURNING id",(medication[i],))
            id = cur.fetchone()[0]
            medication_ids.append(id)
        j=j+1
        for i in range(5):
            cur.execute("INSERT INTO medication_side_effect (severity, probability, side_effect_id, medication_id) VALUES (%s,%s,%s,%s)",(i,"0.8", side_effect_ids[i], medication_ids[i]))

        j=j+1

      

        #insere appointments
        appointment_date=["2024-05-24","2024-04-30","2024-05-21","2024-03-21","2024-06-15"]
        appointment_id = []
        for i in range(5):
            cur.execute("INSERT INTO appointment (ap_date,patient_use_cc,doctor_employee_use_cc, bill_id) VALUES (%s,%s,%s,%s) RETURNING id", (appointment_date[i],pacientes_id[i],medicos_id[i], i+1))
            id = cur.fetchone()[0]
            appointment_id.append(id)
        j=j+1
        #inserir hospitalizações e cirurgias
        #MUDAR TIPO DO ATRIBUTO DURATION
        surgery_date            =["2024-03-4"   ,"2024-02-10"   ,"2024-06-12"   ,"2024-07-17"   ,"2024-06-20"]
        hospitalization_date    =["2024-03-3"   ,"2024-02-9"    ,"2024-06-11"   ,"2024-07-16"   ,"2024-06-19"]
        hospitalization_id = []
        for i in range(5):
            cur.execute("INSERT INTO hospitalization (data_inic, assistant_employee_use_cc, nurse_employee_use_cc, patient_use_cc) VALUES (%s,%s,%s,%s) RETURNING id", (hospitalization_date[i], assistentes_id[i], enfermeiros_id[i], pacientes_id[i]))
            id = cur.fetchone()[0]
            hospitalization_id.append(id)
            cur.execute("INSERT INTO surgery(surgery_date, results, duration, hospitalization_id) VALUES (%s,%s,%s,%s) RETURNING id", (surgery_date[i], "True", (i + 1)*5, id))
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO surgery_nurse (role,nurse_employee_use_cc, surgery_id) VALUES(%s,%s,%s)", ("ajudante", enfermeiros_id[i], id))
        j=j+1
        #insert surgeries
        surgery_date            =["2024-04-4"   ,"2024-05-10"   ,"2024-07-12"   ,"2024-08-17"   ,"2024-07-20"]
        for i in range(5):
            cur.execute("INSERT INTO surgery(surgery_date, results, duration, hospitalization_id) VALUES (%s,%s,%s,%s) RETURNING id",(surgery_date[i], "True",(i+1)*4, hospitalization_id[i]))
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO surgery_nurse (role,nurse_employee_use_cc, surgery_id) VALUES(%s,%s,%s)", ("ajudante", enfermeiros_id[i], id))
        j=j+1
        #add prescriptions
        validades   =["2025-1-1","2026-1-1","2027-1-1","2028-1-1","2029-1-1"]
        frequencia  =["1 vez dia","2 vez dia","3 vez dia","4 vez dia","5 vez dia"]

        for i in range(5):
            cur.execute("INSERT INTO prescription (doctor_employee_use_cc,patient_use_cc,validity) VALUES(%s,%s,%s) RETURNING id",(medicos_id[i], pacientes_id[i], validades[i]))
            id = cur.fetchone()[0]
            cur.execute('INSERT INTO hospitalization_prescription (hospitalization_id,prescription_id) VALUES(%s,%s)', (hospitalization_id[i],id))
            cur.execute('INSERT INTO prescription_medication (dosage,medication_id,frequency,prescription_id) VALUES (%s,%s,%s,%s)',(i+2, medication_ids[i], frequencia[i], id))
            cur.execute('INSERT INTO prescription_appointment (appointment_id,prescription_id) VALUES(%s,%s)',(appointment_id[i],id))
        j=j+1
        conn.commit()
        conn.close()
        response = {'status': StatusCodes['internal_error'], 'success':'yey!'}

    except(Exception,psycopg2.DatabaseError)as error:
        logger.debug(f'start - error: {error}:{j}')
        response = {'status':StatusCodes['internal_error'],'errors': str(error)}
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