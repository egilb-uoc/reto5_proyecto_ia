# reto5_proyecto_ia

Repositorio de soporte para el despliegue serverless realizado en AWS.

## Contenido

- `lambda_function.py`
  - Función AWS Lambda utilizada para:
    - procesar datos del wearable,
    - calcular el SMV,
    - invocar Amazon SageMaker,
    - registrar eventos en DynamoDB,
    - enviar alertas mediante SNS.

- `Compresion_modelo.ipynb`
  - Notebook utilizado para convertir el modelo entrenado en formato `.pkl`
    al formato compatible con Amazon SageMaker Serverless Inference (`model.tar.gz`).
