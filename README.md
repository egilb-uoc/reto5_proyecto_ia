# reto5_proyecto_ia

## Contenido del repositorio

### `lambda_function.py`

Función AWS Lambda utilizada para:

- procesar datos del wearable,
- calcular el SMV,
- invocar Amazon SageMaker,
- registrar eventos en DynamoDB,
- enviar alertas mediante SNS.

#### Variables de entorno utilizadas

- `ENDPOINT_NAME`
  - Nombre del endpoint desplegado en Amazon SageMaker: `endpoint-sisfall-final-v2`

- `TABLE_NAME`
  - Tabla DynamoDB utilizada para registrar alertas: `RegistroAlertas`

- `SNS_TOPIC_ARN`
  - Topic SNS utilizado para el envío de notificaciones: arn:aws:sns:us-east-1:399327635752:AlertasCaidas

---

### `Compresion_modelo.ipynb`

Notebook utilizado para convertir el modelo entrenado en formato `.pkl`
al formato compatible con Amazon SageMaker Serverless Inference (`model.tar.gz`).
