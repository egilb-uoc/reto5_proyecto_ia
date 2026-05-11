import json
import boto3
import math
import os
import time

# Clientes AWS
sagemaker = boto3.client('sagemaker-runtime')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Variables de entorno
    ENDPOINT = os.environ.get('ENDPOINT_NAME')
    TABLE = os.environ.get('TABLE_NAME')
    TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

    try:
        # --- Extracción robusta del payload ---
        if 'body' in event:
            data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            data = event

        # Device ID
        dev_id = data.get('deviceID', 'wearable_01')

        # Features acelerómetro
        ax = float(data['acc_x'])
        ay = float(data['acc_y'])
        az = float(data['acc_z'])

        # Features giroscopio
        gx = float(data['gyro_x'])
        gy = float(data['gyro_y'])
        gz = float(data['gyro_z'])

        # Segundo acelerómetro
        a2x = float(data['acc2_x'])
        a2y = float(data['acc2_y'])
        a2z = float(data['acc2_z'])

        # --- Calcular SMV ---
        smv = math.sqrt(ax**2 + ay**2 + az**2)

        # Payload EXACTO para XGBoost
        payload = f"{ax},{ay},{az},{gx},{gy},{gz},{a2x},{a2y},{a2z},{smv}"
        
        
        # Logs para CloudWatch
        print("Input recibido:", data)
        print("SMV calculado:", smv)
        print("Payload enviado:", payload)

        # --- Invocar SageMaker ---
        resp = sagemaker.invoke_endpoint(
            EndpointName=ENDPOINT,
            ContentType='text/csv',
            Body=payload
        )

        result = resp['Body'].read().decode().strip()
        print("Resultado SageMaker:", result)

        # Convertir predicción
        prob = float(result)
        is_fall = 1 if prob > 0.5 else 0
        status = "FALL DETECTED" if is_fall == 1 else "NORMAL ACTIVITY"

        # --- Persistencia y alertas ---
        if is_fall == 1:
            dynamodb.Table(TABLE).put_item(
                Item={
                    'DeviceID': dev_id,
                    'Timestamp': int(time.time()),
                    'status': status,
                    'smv': str(round(smv, 2))
                }
            )

            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=f"¡ALERTA! Caída detectada en dispositivo: {dev_id}",
                Subject="Emergencia Teleasistencia"
            )

        # --- Respuesta final ---
        return {
            'statusCode': 200,
            'body': json.dumps({
                'prediction': is_fall,
                'status': status,
                'smv': round(smv, 2)
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }