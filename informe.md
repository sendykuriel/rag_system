# Desarrollo y Evaluación de un Sistema RAG

## 1. Introducción

El objetivo de este trabajo práctico es desarrollar y evaluar un sistema de **Retrieval-Augmented Generation (RAG)** sobre una base de conocimiento, siguiendo la consigna de la materia:

- Utilizar una base de conocimiento provista por la cátedra (Greenpeace research) o una propia con al menos 300 documentos.
- Construir un **conjunto de prueba sintético** con al menos 75 preguntas, respuestas y contexto de referencia.
- Implementar y evaluar un **sistema RAG inicial** (similar al visto en clase).
- Diseñar e implementar **al menos 5 nuevas funcionalidades** y realizar **al menos 25 experimentos**, midiendo:

  - Correctitud (Correctness)  
  - Relevancia (Relevance)  
  - Fundamentación / Groundness (Groundness)  
  - Relevancia de la recuperación (Retrieval relevance)

En este informe se presenta:

1. La configuración del sistema RAG utilizado.
2. Las funcionalidades adicionales implementadas.
3. El diseño de los experimentos y los resultados obtenidos.
4. La discusión de resultados y la configuración recomendada final.
5. Un anexo con el detalle de los 25 experimentos realizados.

---

## 2. Sistema RAG y setup experimental

### 2.1. Arquitectura general

El sistema RAG implementado sigue la arquitectura clásica:

1. **Indexado** de la base de conocimiento en forma de *chunks* de texto.
2. **Recuperación** de los documentos más similares a la consulta del usuario mediante un *encoder* de embeddings.
3. **Opcionalmente**: filtrado y re-ranqueo de los documentos recuperados.
4. **Generación** de la respuesta usando un modelo de lenguaje grande (LLM), condicionada por los documentos relevantes.

### 2.2. Configuración base (Experimento 1)

La configuración base del sistema (que se toma como “sistema inicial”) es:

- **Modelo LLM**: `ollama - llama3.1:8b`  
  - Temperatura: `0.7`  
  - Contexto: `4096` tokens  

- **Encoder de embeddings**:  
  - `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`  

- **Recuperación**:
  - Tipo: *similarity search* (búsqueda semántica)  
  - **k documentos recuperados**: `5`  
  - Sin filtrado adicional por LLM (filtrado desactivado)

- **Fragmentación (chunking)**:
  - Estrategia: `RecursiveCharacterTextSplitter` (recursive character splitting)  
  - `chunk_char_size`: `1000`  
  - `chunk_overlap`: `200`  
  - `separators`: `["\n\n", "\n", " ", ""]`

- **Prompt**:
  - Prompt estándar provisto por la cátedra / profesor, donde se le pide al LLM responder usando exclusivamente la información del contexto.

Este setup corresponde al **Experimento 1**, que sirve como línea de base para comparar el efecto de las funcionalidades y cambios de hiperparámetros.

---

## 3. Funcionalidades implementadas

Sobre este sistema base se implementaron **al menos 5 funcionalidades nuevas**, que luego se combinaron y evaluaron en distintos experimentos:

1. **Búsqueda del k óptimo en la recuperación (búsqueda semántica)**  
   - Explorar el impacto en las métricas al variar el número de documentos recuperados `k` (3, 4, 5, 10, 11, 12, 14, 15, 16, 17…).  
   - Experimentos relacionados: 2, 3, 4, 5, 7, 8, 9, 16–20.

2. **Filtrado por LLM de los documentos recuperados (LLM-based filtering)**  
   - Tras la búsqueda por similitud, se aplica un **filtro de relevancia usando el LLM**, que descarta documentos poco útiles antes de generar la respuesta.  
   - Objetivo principal: mejorar la **Retrieval relevance** sin destruir la fundamentación.  
   - Experimentos relacionados: 6, 7, 8, 9, 14–20, 21–25.

3. **Ranqueo mediante expansión de consultas (question expansion + ranking)**  
   - Se generan **preguntas similares adicionales** a partir de la consulta original (por el LLM).  
   - Para cada pregunta se recuperan `k_ranking` documentos; luego se fusionan y ranquean globalmente.  
   - Hiperparámetros:
     - Número de preguntas extra: 3, 5, 7…  
     - `k_ranking`: 2, 3…  
   - Experimentos relacionados: 10, 11, 12, 13, 14–20, 22, 25.

4. **Combinación de ranking + filtrado por LLM**  
   - Pipeline: *similarity search → expansión de preguntas → ranking → filtrado por LLM → generación*.  
   - Objetivo: mejorar correctitud y groundness manteniendo la relevancia de recuperación.  
   - Experimentos relacionados: 14–20, 22, 25.

5. **Modificación de la estrategia de fragmentación (chunking strategy)**  
   - Variación del tamaño del *chunk* y el overlap utilizando el `RecursiveCharacterTextSplitter`.  
   - `chunk_size` probado: 1000 (base), 700, 500, 300.  
   - `chunk_overlap`: típicamente 100–200 caracteres.  
   - Experimentos relacionados: 21, 22, 23, 24, 25.

Estas funcionalidades permitieron diseñar una familia de sistemas RAG con diferente comportamiento frente a las métricas de evaluación.

---

## 4. Diseño de los experimentos

En total se llevaron a cabo **25 experimentos**, agrupados de la siguiente forma:

1. **Exploración de k en la recuperación básica** (Experimentos 1–5)  
   - Mismo chunking y sin filtrado ni ranking adicional.  
   - Objetivo: encontrar un rango razonable de `k` (3–12).

2. **Filtrado por LLM sobre distintas configuraciones de k** (Experimentos 6–9)  
   - Se toma el mejor rango de `k` identificado y se agrega filtrado por LLM.

3. **Ranking con expansión de consultas** (Experimentos 10–13)  
   - Se agregan preguntas similares y re-ranking, variando número de preguntas extra y `k_ranking`.

4. **Ranking + filtrado en combinación con ajuste de k** (Experimentos 14–20)  
   - Se combinan: similarity search, expansión de preguntas, ranking y filtrado, con exploración de k (10–17).

5. **Ajuste de chunking** (Experimentos 21–25)  
   - Se fija una configuración de k y filtrado (inspirada en el Experimento 7, que mostró buen desempeño) y se varía el tamaño de chunk (700, 500, 300) y la presencia de preguntas extra.

En todos los casos se evalúan las métricas:

- **Correctness score**
- **Relevance score**
- **Groundness score**
- **Retrieval relevance score**

sobre el mismo conjunto de pruebas sintético (más de 75 preguntas, tal como requiere la consigna).

---

## 5. Resultados y análisis

### 5.1. Línea de base (Experimento 1)

- **Correctness**: 0.6552  
- **Relevance**: 0.9425  
- **Groundness**: 0.7816  
- **Retrieval relevance**: 0.5517  

Observaciones:

- La **relevancia** ya es alta con la configuración base.
- La **correctitud** y la **fundamentación** son razonables pero con margen de mejora.
- La **relevancia de la recuperación** es la métrica más baja, lo que motiva trabajar sobre la parte de retrieval y filtrado.

---

### 5.2. Variación de k sin filtrado (Experimentos 2–5)

Al variar `k` se observa:

- Para **k = 10 (Experimento 2)**:
  - Correctness: 0.7586  
  - Groundness: 0.8736  
- Para **k = 4 (Experimento 4)**:
  - Correctness: 0.7586  
  - Groundness: 0.9080  

Conclusión:

- Hay un **trade-off** al cambiar `k`: valores bajos y moderados (4–10) funcionan mejor.
- `k=3` empeora la correctitud (Experimento 5).
- De esta primera exploración, **k=4** se considera un buen compromiso.

---

### 5.3. Filtrado por LLM (Experimentos 6–9)

Con filtrado activado:

- **Experimento 6 (k=4 + filtro)**:  
  - Correctness: 0.6897  
  - Retrieval relevance: 0.6552 (mejora respecto a 0.5517)  

- **Experimento 7 (k=10 + filtro)**:  
  - Correctness: **0.8046** (uno de los mejores valores del conjunto)  
  - Relevance: 0.9195  
  - Groundness: 0.8506  
  - Retrieval relevance: 0.5977  

Conclusiones:

- El **filtrado por LLM** mejora claramente la **relevancia de la recuperación**.
- Con **k=10 + filtro** (Experimento 7) se logra una de las mejores combinaciones de correctitud y fundamentación de todo el estudio.

---

### 5.4. Ranking por expansión de consultas (Experimentos 10–13)

Se incorporan preguntas similares y ranking:

- Los cambios de número de preguntas extra y `k_ranking` no produjeron mejoras sistemáticas en **correctness**, y en algunos casos incluso lo reducen.
- La **Retrieval relevance** se mantiene en valores moderados (alrededor de 0.54–0.56).

Conclusión:

- El ranking por expansión de consultas es una funcionalidad interesante, pero **no aporta una mejora clara** en correctitud respecto al mejor modelo con filtrado (Experimento 7).  
- El beneficio parece más marginal y depende del conjunto de preguntas.

---

### 5.5. Combinación ranking + filtrado + ajuste de k (Experimentos 14–20)

Se combinan todas las técnicas:

- Se observa un **pico en Retrieval relevance** con `k = 16–17`:
  - Experimento 19 (k=16): Retrieval relevance: 0.7126  
  - Experimento 20 (k=17): Retrieval relevance: 0.7126  

- Sin embargo:
  - Correctness en esos experimentos está entre 0.7241 y 0.7471, por debajo del máximo de 0.8046 del Experimento 7.
  - Groundness se mantiene alta, pero con cierto desgaste al seguir subiendo k.

Conclusión:

- Es posible **maximizar la relevancia de la recuperación** con k muy altos, pero a costa de complejidad y sin un aumento claro en correctitud.
- En términos prácticos, el **Experimento 7** sigue siendo muy competitivo como punto de equilibrio.

---

### 5.6. Ajuste de chunking (Experimentos 21–25)

Tomando la configuración “buena” (k=10 + filtro) se varía el tamaño de chunk:

- **Experimento 21 (chunk=700, sin preguntas extra)**:
  - Correctness: 0.7816  
  - Groundness: 0.8851  
  - Retrieval relevance: 0.5402  

- **Experimento 23 (chunk=500, sin preguntas extra)**:
  - Correctness: 0.7816  
  - Groundness: 0.8966  
  - Retrieval relevance: 0.5402  

- **Experimento 24 (chunk=300)**:
  - Correctness: 0.7701  
  - Groundness: 0.8851  
  - Retrieval relevance: 0.4828  

Y con chunk=500 pero con preguntas extra y filtro (Experimento 25):

- Correctness: 0.7356  
- Relevance: 0.9425  
- Groundness: 0.8736  
- Retrieval relevance: 0.5057  

Conclusiones:

- **Chunks intermedios (500–700 caracteres)** funcionan mejor que los muy grandes (1000) o muy pequeños (300).
- La combinación de chunk=500, k=10 y filtrado mantiene buena correctitud y fundamentación sin empeorar demasiado la recuperación.
- Agregar preguntas extra sobre este setup (Experimento 25) no mejora la correctitud.

---

## 6. Configuración final recomendada

A partir de los resultados, se proponen **dos configuraciones recomendadas** según el criterio de optimización:

### 6.1. Configuración orientada a máxima Correctitud

Basada en el **Experimento 7**:

- **LLM**: `ollama - llama3.1:8b` (temp 0.7, context 4096)
- **Encoder**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Recuperación**:
  - Similarity search con `k = 10`
  - Filtrado de relevancia por LLM **activado**
- **Chunking**:
  - `RecursiveCharacterTextSplitter`
  - `chunk_size`: 1000
  - `chunk_overlap`: 200

Métricas (Exp. 7):

- Correctness: **0.8046**  
- Relevance: 0.9195  
- Groundness: 0.8506  
- Retrieval relevance: 0.5977  

Esta configuración es adecuada cuando se prioriza la **calidad de la respuesta** (correctitud y fundamentación) por sobre la máxima cobertura posible de la base de conocimiento.

---

### 6.2. Configuración orientada a equilibrio Correctitud / Groundness / Eficiencia

Basada en los **Experimentos 21 y 23**:

- **LLM**: `ollama - llama3.1:8b`
- **Encoder**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Recuperación**:
  - Similarity search con `k = 10`
  - Filtrado de relevancia por LLM **activado**
- **Chunking**:
  - `RecursiveCharacterTextSplitter`
  - `chunk_size`: 500
  - `chunk_overlap`: 100

Métricas (Exp. 23):

- Correctness: 0.7816  
- Relevance: 0.9310  
- Groundness: 0.8966  
- Retrieval relevance: 0.5402  

Esta configuración es un **buen compromiso** entre correctitud, fundamentación y eficiencia del sistema, y puede ser preferible para un entorno productivo.

---

## 7. Conclusiones

En este trabajo se desarrolló y evaluó un sistema RAG completo, cumpliendo con los requisitos de la cátedra:

- Se construyó un conjunto de pruebas sintético con más de 75 preguntas, respuestas y contexto.
- Se evaluó un sistema RAG inicial y se definió una línea de base.
- Se implementaron **más de 5 funcionalidades nuevas** (búsqueda de k óptimo, filtrado por LLM, ranking con expansión de consultas, combinación ranking+filtrado, ajuste de chunking).
- Se realizaron **25 experimentos** variando hiperparámetros y componentes del pipeline.

Algunas conclusiones principales:

1. **Filtrado por LLM** sobre los documentos recuperados es una de las técnicas que más aporta a la mejora de correctitud y relevancia de la recuperación.
2. La elección de `k` es crítica:
   - Valores demasiado bajos pierden contexto.
   - Valores muy altos aumentan ruido y complejidad.
   - En este caso, `k ≈ 10` resultó un valor razonable.
3. La **estrategia de fragmentación** impacta en cómo el modelo aprovecha el contexto:
   - Chunks demasiado grandes dificultan el enfoque del LLM.
   - Chunks demasiado pequeños fragmentan la información.
   - En este experimento, `chunk_size = 500–700` funciona bien.
4. Las técnicas de **expansión de consultas y ranking** no mostraron mejoras claras en correctitud sobre este conjunto de pruebas, aunque sí son prometedoras para escenarios con consultas más ambiguas o multi-tópico.
