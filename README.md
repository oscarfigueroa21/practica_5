# Práctica 5: Normalización de Datos y Reducción de Dimensionalidad. Visualización de Datos

## Objetivo del Proyecto
El objetivo de esta práctica es preparar un dataset para su posterior uso en el entrenamiento de un modelo de aprendizaje automático. Para ello, se aplicará el preprocesamiento de datos visto en las prácticas 3 y 4, la normalización de datos numéricos, reducción de dimensionalidad mediante el uso de PCA. 
La visualización se hara mediante un dashbord interactivo que permita la exploración de los datos y su comunicación. 

## Fuente de los Datos
Los datos utilizados para la elaboración de esta práctica, se pueden encontrar y descargar desde la página: [Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
Una vez descargado el dataset, este debe colocarse en la carpeta `data/data-raw/` para su reproducción. 

* *Nota:* Por políticas de tamaño de Git, el archivo original txt contenido en `data/data-raw/` no se incluye en el repositorio.

## Estructura de Carpetas
Esta práctica posee una estructura de carpetas idéntica a las realizadas en las dos prácticas anteriores. Se incluyen dos nuevas carpetas llamadas `visualization` y `dashbord`. 


## Dataset Procesado
El dataset preparado final se guardó en `data/data-processed/consumo_preparado.parquet`. Se utilizó el formato Parquet en lugar de CSV para optimizar el almacenamiento (pesa ~90 MB frente a los ~190 MB que ocuparía en CSV plano), permitiendo subirlo directamente al repositorio dentro del límite de GitHub y agilizar su lectura en el dashboard.

## Cómo instalar el entorno
Este proyecto utiliza Python 3.10+ y los frameworks `pandas`, `matplotlib`, `sckit-learn`, `stremlit`.

1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activar el entorno virtual (Linux/Mac: `source venv/bin/activate` | Windows: `venv\Scripts\activate`)
4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt

## Cómo ejecutar el pipeline
La inspección, limpieza, normalización, y los análisis dimensionalidad estan dividido por temáticas en las carpetas correspondientes, según la rúbrica de la práctica:

1. **Inspección:** Ejecutar `notebooks/Inspeccion.ipynb` (incluye carga de datos, dimensiones, tipos de datos y problemas de calidad econtrados. ).
2. **Limpieza y Normalización:** Ejecutar `src/cleaning/limpieza.ipynb` (Incluye casteo de datos, deduplicación, imputación de nulos y normalización.)
3. **Correlación de Pearson:** Ejecutar `notebooks/dimensionalidad.ipynb` (Incluye matriz de correlación de Pearson de las variables cuantitativas, eliminación de variables con alta correlación. ).
4. **Analisis de Componentes Principales (PCA):** Ejecutar `notebooks/analisis_PCA.ipynb` (Analisis PCA con la gráfica de varianza y proyección 2D).
