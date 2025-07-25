# Estructura de Supabase

### **`Categoria_Emisor`**

* **Nombre de la Tabla:** `Categoria_Emisor`  
* **Columnas:**  
  * `id_categoria_emisor`: INT (PK)  
  * `categoria_emisor`: VARCHAR(100)

### **2\. `Emisores`**

* **Nombre de la Tabla:** `Emisores`  
* **Columnas:**  
  * `id_emisor`: INT (PK)  
  * `nombre_emisor`: VARCHAR(250)  
  * `id_categoria_emisor`: INT (FK)  
  * `calificacion_bva`: VARCHAR(100)

### **3\. `Moneda`**

* **Nombre de la Tabla:** `Moneda`  
* **Columnas:**  
  * `id_moneda`: INT (PK)  
  * `codigo_moneda`: VARCHAR(10)  
  * `nombre_moneda`: VARCHAR(50)

### **4\. `Frecuencia`**

* **Nombre de la Tabla:** `Frecuencia`  
* **Columnas:**  
  * `id_frecuencia`: INT (PK)  
  * `nombre_frecuencia`: VARCHAR(50)

### **5\. `Tipo_Informe`**

* **Nombre de la Tabla:** `Tipo_Informe`  
* **Columnas:**  
  * `id_tipo_informe`: INT (PK)  
  * `nombre_tipo_informe`: VARCHAR(100)

### **6\. `Periodo_Informe`**

* **Nombre de la Tabla:** `Periodo_Informe`  
* **Columnas:**  
  * `id_periodo`: INT (PK)  
  * `nombre_periodo`: VARCHAR(50)

### **7\. `Unidad_Medida`**

* **Nombre de la Tabla:** `Unidad_Medida`  
* **Columnas:**  
  * `id_unidad_medida`: INT (PK)  
  * `simbolo`: VARCHAR(10)  
  * `nombre_unidad`: VARCHAR(50)

### **8\. `Fuente_Noticia`**

* **Nombre de la Tabla:** `Fuente_Noticia`  
* **Columnas:**  
  * `id_fuente_noticia`: INT (PK)  
  * `nombre_fuente`: VARCHAR(250)

### **9\. `Instrumento`**

* **Nombre de la Tabla:** `Instrumento`  
* **Columnas:**  
  * `id_instrumento`: INT (PK)  
  * `simbolo_instrumento`: VARCHAR(50)  
  * `nombre_instrumento`: VARCHAR(255)

### **10\. `Informe_General`**

* **Nombre de la Tabla:** `Informe_General`  
* **Columnas:**  
  * `id_informe`: INT (PK)  
  * `id_emisor`: INT (FK, NULLABLE)  
  * `id_tipo_informe`: INT (FK)  
  * `id_frecuencia`: INT (FK, NULLABLE)  
  * `id_periodo`: INT (FK, NULLABLE)  
  * `titulo_informe`: VARCHAR(500)  
  * `resumen_informe`: TEXT (NULLABLE)  
  * `fecha_publicacion`: DATE  
  * `url_descarga_original`: VARCHAR(500) (NULLABLE)  
  * `detalles_informe_jsonb`: JSONB (NULLABLE)

### **11\. `Resumen_Informe_Financiero`**

* **Nombre de la Tabla:** `Resumen_Informe_Financiero`  
* **Columnas:**  
  * `id_resumen_financiero`: INT (PK)  
  * `id_informe`: INT (FK)  
  * `id_emisor`: INT (FK)  
  * `fecha_corte_informe`: DATE  
  * `moneda_informe`: INT (FK)  
  * `activos_totales`: DECIMAL (NULLABLE)  
  * `pasivos_totales`: DECIMAL (NULLABLE)  
  * `patrimonio_neto`: DECIMAL (NULLABLE)  
  * `disponible`: DECIMAL (NULLABLE)  
  * `utilidad_del_ejercicio`: DECIMAL (NULLABLE)  
  * `ingresos_totales`: DECIMAL (NULLABLE)  
  * `costos_operacionales`: DECIMAL (NULLABLE)  
  * `total_ganancias`: DECIMAL (NULLABLE)  
  * `total_perdidas`: DECIMAL (NULLABLE)  
  * `retorno_sobre_patrimonio`: DECIMAL (NULLABLE)  
  * `calificacion_riesgo_tendencia`: VARCHAR(100) (NULLABLE)  
  * `utilidad_neta_por_accion_ordinaria`: DECIMAL (NULLABLE)  
  * `deuda_total`: DECIMAL (NULLABLE)  
  * `ebitda`: DECIMAL (NULLABLE)  
  * `margen_neto`: DECIMAL (NULLABLE)  
  * `flujo_caja_operativo`: DECIMAL (NULLABLE)  
  * `capital_integrado`: DECIMAL (NULLABLE)  
  * `otras_metricas_jsonb`: JSONB (NULLABLE)

### **12\. `Dato_Macroeconomico`**

* **Nombre de la Tabla:** `Dato_Macroeconomico`  
* **Columnas:**  
  * `id_dato_macro`: INT (PK)  
  * `id_informe`: INT (FK, NULLABLE)  
  * `indicador_nombre`: VARCHAR(250)  
  * `fecha_dato`: DATE  
  * `valor_numerico`: DECIMAL  
  * `unidad_medida`: INT (FK, NULLABLE)  
  * `id_frecuencia`: INT (FK)  
  * `link_fuente_especifico`: VARCHAR(500) (NULLABLE)  
  * `otras_propiedades_jsonb`: JSONB (NULLABLE)  
  * `id_moneda`: INT (FK, NULLABLE)  
  * `id_emisor`: INT (FK, NULLABLE)

### **13\. `Movimiento_Diario_Bolsa`**

* **Nombre de la Tabla:** `Movimiento_Diario_Bolsa`  
* **Columnas:**  
  * `id_operacion`: INT (PK)  
  * `fecha_operacion`: DATE  
  * `cantidad_operacion`: DECIMAL  
  * `id_instrumento`: INT (FK)  
  * `id_emisor`: INT (FK)  
  * `fecha_vencimiento_instrumento`: DATE (NULLABLE)  
  * `id_moneda`: INT (FK)  
  * `precio_operacion`: DECIMAL  
  * `precio_anterior_instrumento`: DECIMAL (NULLABLE)  
  * `tasa_interes_nominal`: DECIMAL (NULLABLE)  
  * `tipo_cambio`: DECIMAL (NULLABLE)  
  * `variacion_operacion`: DECIMAL (NULLABLE)  
  * `volumen_gs_operacion`: DECIMAL (NULLABLE)

### **14\. `Licitacion_Contrato`**

* **Nombre de la Tabla:** `Licitacion_Contrato`  
* **Columnas:**  
  * `id_licitacion_contrato`: INT (PK)  
  * `id_emisor_adjudicado`: INT (FK, NULLABLE)  
  * `titulo`: VARCHAR(500)  
  * `entidad_convocante`: VARCHAR(255) (NULLABLE)  
  * `monto_adjudicado`: DECIMAL (NULLABLE)  
  * `id_moneda`: INT (FK, NULLABLE)  
  * `fecha_adjudicacion`: DATE (NULLABLE)

# Estructura de Pinecone

Your Pinecone setup will consist of four separate indexes, each corresponding to a collection in your vector database design. All indexes will use the same embedding model's dimensions and metric.

### **Common Configuration for All Indexes:**

* **Dimensions:** 384 (for `sentence-transformers/all-MiniLM-L6-v2` embeddings)  
* **Metric:** `cosine`  
* **Capacity Mode:** `Serverless` (for free tier)  
* **Cloud Provider:** AWS (or other available on your plan)  
* **Region:** `us-east-1` (or your chosen region)

---

### **1\. Index: `documentos-informes-vector`**

* **Purpose:** Stores embeddings for full reports, studies, and extensive documents.  
* **Metadatos esperados por vector (al momento de la inserción):**  
  * `id_informe`: INT  
  * `id_emisor`: INT, NULLABLE  
  * `id_tipo_informe`: INT  
  * `id_frecuencia`: INT  
  * `id_periodo`: INT, NULLABLE  
  * `fecha_publicacion`: DATE  
  * `chunk_id`: INT  
  * `chunk_text`: TEXT

---

### **2\. Index: `noticia-relevante-vector`**

* **Purpose:** Stores embeddings for news articles.  
* **Metadatos esperados por vector:**  
  * `id_noticia`: INT  
  * `id_emisor`: INT  
  * `id_fuente_noticia`: INT  
  * `fecha_publicacion`: DATE  
  * `chunk_id`: INT  
  * `chunk_text`: TEXT

---

### **3\. Index: `dato-macroeconomico-vector`**

* **Purpose:** Stores embeddings for contextual text around macroeconomic data points.  
* **Metadatos esperados por vector:**  
  * `id_dato_macro`: INT  
  * `indicador_nombre`: VARCHAR(250)  
  * `fecha_dato`: DATE  
  * `id_unidad_medida`: INT, NULLABLE  
  * `id_moneda`: INT, NULLABLE  
  * `id_frecuencia`: INT, NULLABLE  
  * `id_emisor`: INT, NULLABLE  
  * `id_informe`: INT, NULLABLE  
  * `chunk_id`: INT  
  * `chunk_text`: TEXT

---

### **4\. Index: `licitacion-contrato-vector`**

* **Purpose:** Stores embeddings for detailed information about licitations and contracts.  
* **Metadatos esperados por vector:**  
  * `id_licitacion_contrato`: INT  
  * `titulo`: VARCHAR(500)  
  * `id_emisor_adjudicado`: INT  
  * `entidad_convocante`: VARCHAR(255), NULLABLE  
  * `monto_adjudicado`: DECIMAL, NULLABLE  
  * `id_moneda`: INT  
  * `fecha_adjudicacion`: DATE  
  * `chunk_id`: INT  
  * `chunk_text`: TEXT

