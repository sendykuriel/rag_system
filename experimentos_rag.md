# Memoria de Experimentos en RAG

## Experimento 1

### Parámetros Utilizados

- **Modelo LLM** : ollama - llama3.1:8b - (temp 0.7, context 4096 tkns)
- **Encoder** : sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **k archivos recuperados**: 5
- **Forma de los chunks**: Recursive character splitting
- **Parámetros de chunking**: 
  - `chunk_char_size`: 1000
  - `chunk_overlap`: 200
  - `separators`: ["\n\n", "\n", " ", ""]
- **Tipo de recuperación**: Similarity search con filtrado por LLM
- **Filtrado**; Desactivado
- **Prompt**: Estandar (provisto por el profesor)

### Resultados Obtenidos
- Correctness score: 0.6551724137931034
- Relevance score: 0.9425287356321839
- Groundness score: 0.7816091954022989
- Retrieval relevance score: 0.5517241379310345

## Experimento 2

### Detalle

    Se busca mejorar cambiando recuperacion a 10

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.7586206896551724
- **Relevance score**: 0.9080459770114943
- **Groundness score**: 0.8735632183908046
- **Retrieval relevance score**: 0.5287356321839081

## Experimento 3

### Detalle

    Se ve que mejoro el correctness y el groundness. Pruebo subir un poco mas la cantidad de recuperados. Pasamos a k=12

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.7471264367816092
- **Relevance score**: 0.896551724137931
- **Groundness score**: 0.9655172413793104
- **Retrieval relevance score**:0.6091954022988506

## Experimento 4

### Detalle

    El correctnes del experimento anterior bajo. 
    Probamos bajar la cantidad de recuperacion (<5) para comparar el efecto vs haber subido.
    Pruebo k=4.
    Resultado bastante similar que el experimento 2. 

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.7586206896551724
- **Relevance score**:0.8735632183908046
- **Groundness score**:0.9080459770114943
- **Retrieval relevance score**:0.5517241379310345

## Experimento 5

### Detalle

    Pruebo k=3 a ver si mejora o el optimo esta dentro de k=4 o k=10

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6551724137931034
- **Relevance score**:0.896551724137931
- **Groundness score**:0.8850574712643678
- **Retrieval relevance score**:0.5287356321839081

## Experimento 6

    Con el k optimo obtenido (k=4) probamos agregar un filtro de relevancia (LLM). Dado que queremos ver si podemos mejorar el Retrieval relevance score (que es relativamente el valor mas bajo)

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6896551724137931
- **Relevance score**:0.9310344827586207
- **Groundness score**:0.8505747126436781
- **Retrieval relevance score**:0.6551724137931034

## Experimento 7
    Pruebo con un k mayor (k=10) y con filtro. Quizas si le damos mas opciones al filtro (trayendo mas documentos) encuentra mejores cosas.       

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.8045977011494253
- **Relevance score**: 0.9195402298850575
- **Groundness score**:0.8505747126436781
- **Retrieval relevance score**:0.5977011494252874

## Experimento 8

- Pruebo con un k aun mayor (k=12) y con filtro. Quizas si le damos mas opciones al filtro (trayendo mas documentos) encuentra mejores cosas. 

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.7471264367816092
- **Relevance score**:0.8850574712643678
- **Groundness score**:0.9425287356321839
- **Retrieval relevance score**:0.4827586206896552

## Experimento 9

- k=12 mejoro algunas metricas pero no corectness. y claramente empeora el retrieval.  Pruebo con k = 11 para ver  


### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.7241379310344828
- **Relevance score**:0.8850574712643678
- **Groundness score**:0.896551724137931
- **Retrieval relevance score**:0.5862068965517241

## Experimento 10

    Volvemos a k=10
    Rankeo: implementar generacion de 5 preguntas similares. Luego hacer el retreive de esas 5. 
    Cantidad de preguntas extra = 5.
    k_ranking (cuantos docs por cada pregunta) = 2 .

    - Primero sin filtrado por llm sino que solamente por ranking. (luego a este rank le aplicaremos filtrado tambien)
    -Buscamos primero optimizar hiper parametros del rank. (cantidad de preguntas y textos por pregunta)

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.7126436781609196
- **Relevance score**: 0.8850574712643678
- **Groundness score**: 0.9310344827586207
- **Retrieval relevance score**: 0.5402298850574713

## Experimento 11
    Probamos otros parammetros de rankeo
    - Preguntas extra = 5 
    - k_ranking = 3 (aumentamos)
   
    
### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6666666666666666
- **Relevance score**: 0.8735632183908046
- **Groundness score**: 0.9195402298850575
- **Retrieval relevance score**: 0.45977011494252873

## Experimento 12
    Probamos otros parammetros de rankeo (en el anterior no hubo mejoras)
        - Preguntas extra = 7 (aumentamos)
        - k_ranking = 2 (volvemos al original)
 
### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6551724137931034
- **Relevance score**: 0.8735632183908046
- **Groundness score**: 0.8620689655172413
- **Retrieval relevance score**: 0.5632183908045977

## Experimento 13

    Probamos otros parammetros de rankeo (en el anterior no hubo mejoras)
        - Preguntas extra = 3 (bajamos)
        - k_ranking = 2 (volvemos al original)

    

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6551724137931034
- **Relevance score**: 0.8390804597701149
- **Groundness score**: 0.8505747126436781
- **Retrieval relevance score**: 0.5402298850574713

## Experimento 14

    Lo mejor habia sido k=10 con filtro. Ahora vamos por esto mismo sumado al extra de preguntas (es decir prendemos el filtrado)
    Cantidad de preguntas extra = 5.
    k_ranking (cuantos docs por cada pregunta) = 2 .

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.6896551724137931
- **Relevance score**: 0.8275862068965517
- **Groundness score**: 0.896551724137931
- **Retrieval relevance score**: 0.5057471264367817

## Experimento 15

    Que pasa si bajamos el k=5 (similarity_score) ? Manteniendo esto (preguntas extra y filtrado).


### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.5632183908045977
- **Relevance score**:0.8160919540229885
- **Retrieval relevance score**:0.5402298850574713

## Experimento 16

    Que pasa su lo subimos a k=12

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.7011494252873564
- **Relevance score**:0.8850574712643678
- **Groundness score**:0.8045977011494253
- **Retrieval relevance score**:0.5172413793103449

## Experimento 17

    Dado que mejoro (un poco) podemos probar subiendo el k un poco mas (aunque estimo no creo mejore y quizas ya se pierda mucho ground)
    k=14

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.7241379310344828
- **Relevance score**: 0.9195402298850575
- **Groundness score**: 0.896551724137931
- **Retrieval relevance score**: 0.5402298850574713

## Experimento 18

    Los valores mejoraron, asi que pruebo otro k aun mayor k=15.

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.6551724137931034
- **Relevance score**:0.896551724137931
- **Groundness score**:0.9425287356321839
- **Retrieval relevance score**:0.5862068965517241

## Experimento 19

    empeoraron los valores. por las dudas pruebo k16

### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**:0.7471264367816092
- **Relevance score**:0.8620689655172413
- **Groundness score**:0.9080459770114943
- **Retrieval relevance score**:0.7126436781609196

## Experimento 20

    -Probamos con k17 a ver si encontramos ya que baja o hay otro maximo. Subio tanto correctness como el retrieval relevance score. 
    Ta el correctness no mejora. 
### Parámetros Utilizados

### Resultados Obtenidos

- **Correctness score**: 0.7241379310344828
- **Relevance score**: 0.8850574712643678
- **Groundness score**:0.8275862068965517
- **Retrieval relevance score**:0.7126436781609196


## Experimento 21

 - Tomamos los parametros del experimento 7 
  (k=10 y con filtro, sin preguntas extra)
 - Trabajamos con los chunks (fragmentación):Probar chunk_size = 700 (recursivo)

### Resultados Obtenidos

- **Correctness score**: 0.7816091954022989
- **Relevance score**:0.896551724137931
- **Groundness score**:0.8850574712643678
- **Retrieval relevance score**:0.5402298850574713

## Experimento 22


 - Tomamos los parametros del experimento 7 
  (k=10 y con filtro, con preguntas extra)
 - Trabajamos con los chunks (fragmentación):Probar chunk_size = 700 (recursivo)

### Resultados Obtenidos

- **Correctness score**: 0.632183908045977
- **Relevance score**: 0.9310344827586207
- **Groundness score**: 0.8160919540229885
- **Retrieval relevance score**: 0.5632183908045977

## Experimento 23


No resulto mejor el correctness con las preguntas.
Probamos con achicacar el chunck.
 - Tomamos los parametros del experimento 7 
  (k=10 y con filtro, sin preguntas extra)
 - Trabajamos con los chunks (fragmentación):Probar chunk_size = 500 (recursivo) (y 100 de overlap)

### Resultados Obtenidos

- **Correctness score**:  0.7816091954022989
- **Relevance score**: 0.9310344827586207
- **Groundness score**:0.896551724137931
- **Retrieval relevance score**:0.5402298850574713

## Experimento 24

Lo mismo pero con chunk de 300 

### Resultados Obtenidos

- **Correctness score**: 0.7701149425287356
- **Relevance score**: 0.8735632183908046
- **Groundness score**: 0.8850574712643678
- **Retrieval relevance score**:0.4827586206896552

## Experimento 25

500 resulto ser mejor. Entonces dejamos 500 de chunk y probamos con filtro y preguntas extra. 

### Resultados Obtenidos

- **Correctness score**: 0.735632183908046
- **Relevance score**:0.9425287356321839
- **Groundness score**:0.8735632183908046
- **Retrieval relevance score**:0.5057471264367817



