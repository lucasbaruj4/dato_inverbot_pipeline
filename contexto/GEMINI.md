Contexto del Proyecto CrewAI: Base de Conocimiento para Gemini



Este documento provee contexto extendido para el modelo Gemini, complementando el input directo.



1\. Instrucciones del Proyecto



Objetivo Central



Construir un sistema de IA multi-agente (CrewAI) que automatice la investigación de mercado, la estructuración de datos y la vectorización, culminando en un reporte analítico.



Fase Actual (Desarrollo y Población Inicial)











Configuración de Infraestructura: Conectar a PostgreSQL (Supabase) y Pinecone.







Herramientas Custom: Desarrollar herramientas Python para agentes (insertar en PostgreSQL, vectorizar y almacenar en Pinecone).







Pipeline de Ingesta (CrewAI):











Agentes (Researcher, Extractor/Parser) adquieren contenido de fuentes (indicadas por el usuario).







Extraen inteligentemente datos estructurados para poblar tablas de PostgreSQL (incluyendo lookup tables).







Preparan texto y metadatos para vectorización.







Vectorizan y almacenan en Pinecone (colecciones: documento\_informe\_vector, noticia\_relevante\_vector, dato\_macroeconomico\_vector, licitacion\_contrato\_vector).







Propósito: Poblar automáticamente ambas bases de datos desde el inicio.



Tecnologías Clave











Orquestación de Agentes: CrewAI







LLM para Agentes: mistralai/Mistral-7B-Instruct-v0.3 (ejecución local en Colab T4 GPU)







Base de Datos Estructurada: PostgreSQL (en Supabase)







Base de Datos Vectorial: Pinecone







Modelo de Embeddings: sentence-transformers/all-MiniLM-L6-v2







Herramientas de Adquisición: SerperDevTool, FirecrawlSearchTool, FirecrawlScrapeWebsiteTool



2\. Requerimientos de Seguridad en la Construcción











API Keys: Siempre deben ser cargadas desde Google Colab Secrets (variables de entorno), nunca codificadas directamente.







Credenciales DB: Mantener las credenciales de PostgreSQL (Supabase) y Pinecone seguras, cargándolas también desde Colab Secrets.







Acceso a Datos: Restringir el acceso a la base de datos solo a las operaciones necesarias para la ingesta.







Privacidad: Considerar la privacidad de cualquier dato sensible extraído.



3\. Reglas sobre Eliminar Recursos/Datos











¡CRÍTICO!











NO ELIMINAR tablas de la base de datos (PostgreSQL, Pinecone) sin confirmación explícita y separada del usuario.







NO ELIMINAR registros de datos de ninguna tabla (ni estructurada ni vectorial) sin confirmación explícita del usuario.







NO MODIFICAR o SOBREESCRIBIR datos existentes sin una lógica clara de actualización y permiso.







Priorizar la integridad y persistencia de los datos.



4\. Principios Operacionales Clave











Clarificación y Datos Críticos: Siempre pregunta al usuario sobre datos que no sepas o que sean críticos para avanzar. No asumas ni infieras sin consulta. 🤔







Evitar Alucinaciones (Veracidad): Responde y extrae información siempre en base a datos reales y verificables. No inventes ni generes información no soportada por la evidencia. La fiabilidad es primordial. ✅







Uso de Documentación de Herramientas: Para entender cómo trabajar con herramientas o librerías específicas (ej. crewai-tools, psycopg2, pinecone-client), siempre consulta directamente sus documentaciones oficiales o ejemplos confirmados. No inventes su uso. 📖



5\. Links a Documentación Relevante











CrewAI Docs: https://docs.crewai.com/







Pinecone Docs: https://docs.pinecone.io/







Supabase (PostgreSQL) Docs: https://supabase.com/docs/guides/database







Hugging Face Hub (Tokens \& Models): https://huggingface.co/docs/hub/security-tokens







sentence-transformers Docs: https://www.sbert.net/







Firecrawl Docs: https://firecrawl.dev/docs







SerperDevTool (crewai-tools): (Refer to crewai-tools docs or examples for specific usage)

