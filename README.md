# reto5_proyecto_ia

# - `lambda_function.py`
  - Función AWS Lambda utilizada para:
    - procesar datos del wearable,
    - calcular el SMV,
    - invocar Amazon SageMaker,
    - registrar eventos en DynamoDB,
    - enviar alertas mediante SNS.
    - Variables de entorno utilizadas

            - `ENDPOINT_NAME`
              - Nombre del endpoint desplegado en Amazon SageMaker.
            
            - `TABLE_NAME`
              - Tabla DynamoDB utilizada para registrar alertas.
            
            - `SNS_TOPIC_ARN`
              - Topic SNS utilizado para el envío de notificaciones.
      

# - `Compresion_modelo.ipynb`
  - Notebook utilizado para convertir el modelo entrenado en formato `.pkl`
    al formato compatible con Amazon SageMaker Serverless Inference (`model.tar.gz`).
