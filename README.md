**Examen Final  Python API Developer**

**PARTE TEORICA (10 PUNTOS)** 

1\. Para qué se puede usar Python en lo que respecta a datos. Dar 5 casos y explicar brevemente 

Python es el lenguaje dominante en el mundo de los datos gracias a su sintaxis clara y su vasto ecosistema de librerías. 5 casos clave:

|**Caso de Uso**|**Librerías Típicas**|**Explicación Breve**|
| :- | :- | :- |
|**1. Ciencia de Datos y Análisis**|NumPy, Pandas|Pandas permite cargar, limpiar, transformar y analizar grandes conjuntos de datos de manera eficiente (Data Wrangling), sirviendo de base para cualquier análisis estadístico posterior.|
|**2. Aprendizaje Automático (ML)**|Scikit-learn, TensorFlow, PyTorch|Python se usa para construir, entrenar y evaluar modelos predictivos (clasificación, regresión) que aprenden patrones a partir de los datos.|
|**3. Web Scraping y Recolección**|Beautiful Soup, Scrapy|Permite automatizar la extracción estructurada de grandes volúmenes de datos de sitios web, convirtiendo HTML desestructurado en datos limpios para análisis.|
|**4. Visualización de Datos**|Matplotlib, Seaborn|Se utiliza para generar gráficos estáticos, interactivos y dinámicos (histogramas, diagramas de dispersión, mapas de calor) que facilitan la comprensión de las tendencias en los datos.|
|**5. Ingeniería de Datos (ETL)**|Apache Spark (PySpark), Airflow|Se utiliza para construir *pipelines* robustos (procesos ETL/ELT) para extraer datos de múltiples fuentes, transformarlos y cargarlos en almacenes de datos.|

2\. ¿Cómo se diferencian Flask de Django? Argumentar. 

La diferencia principal radica en el **alcance** y la **filosofía de diseño**:

|**Característica**|**Flask (Micro-framework)**|**Django (Full-stack Framework)**|
| :- | :- | :- |
|**Filosofía**|Minimalista, "Hacerlo tú mismo" (DIY).|Baterías Incluidas ("Batteries Included").|
|**Alcance**|Ideal para APIs, microservicios y proyectos pequeños que requieren flexibilidad.|Ideal para aplicaciones complejas, bases de datos múltiples y proyectos empresariales.|
|**Componentes**|No incluye ORM, autenticación o formularios por defecto.|Incluye ORM, panel de administración, autenticación y plantillas como estándar.|


**Argumento:** **Flask** ofrece **libertad total** para elegir cada componente externo. **Django** ofrece una **convención** preestablecida y herramientas completas, acelerando proyectos grandes a costa de reducir la flexibilidad.

3\. ¿Qué es un API? Explicar en sus propias palabras 

**API** significa **I**nterfaz de **P**rogramación de **A**plicaciones.

Es un **contrato digital** que define las reglas y el formato (los *endpoints*) que un sistema debe seguir para solicitar o enviar datos a otro sistema. Actúa como un **mensajero o intermediario** que permite que dos piezas de *software* se comuniquen sin que una sepa cómo está construida la otra.

Si mi aplicación (el **cliente**) necesita una lista de productos, llama al *endpoint* de la API (el **contrato**) y la API le devuelve los datos en un formato estándar (generalmente JSON).

4\. ¿Cuál es la principal diferencia entre REST y WebSockets? 

La distinción clave es el **modelo de comunicación** y la **persistencia de la conexión**:

|Característica|REST|WebSockets|
| :- | :- | :- |
|**Conexión**|Sin estado (Stateless) y de vida corta.|Con estado (Stateful) y persistente (vida larga).|
|**Modelo**|Cliente inicia la solicitud; Servidor responde. (Unidireccional por transacción).|Una vez abierta, ambas partes envían datos en cualquier momento. (Bidireccional y continua).|
|**Uso Principal**|Transacciones (CRUD), documentos, servicios estándar.|Datos en tiempo real, *chats*, notificaciones, *streaming*.|

**Principal Diferencia:** **REST** usa solicitudes discretas e independientes. **WebSockets** abre un **canal persistente** que permite la comunicación instantánea en ambos sentidos.

5\. Describir un ejemplo de API comercial y como funciona – usar otros ejemplos no vistos en el curso. 

**Ejemplo:** **API de Stripe para Pagos (Stripe Payments API)**

Stripe es una plataforma que permite a empresas procesar pagos en línea sin tener que manejar directamente datos sensibles de tarjetas de crédito o cumplir con las regulaciones de seguridad financiera (PCI compliance).

**Cómo Funciona:**

1. **Solicitud de Pago:** Cuando un usuario hace clic en "Comprar" en una tienda en línea, el servidor de la tienda (tu *backend* de FastAPI) envía una solicitud POST a la API de Stripe. Esta solicitud incluye el monto, la divisa y un *token* seguro que representa la tarjeta de crédito del usuario.
1. **Procesamiento:** El servidor de Stripe se comunica con los bancos y las redes de tarjetas (Visa/Mastercard) para:
   1. **Autenticar** y **autorizar** la transacción.
   1. **Manejar la seguridad** (cifrado, prevención de fraude).
1. **Respuesta:** Stripe devuelve una respuesta JSON a tu servidor:
   1. Si es exitosa, incluye un objeto de "Transacción" con el estado **succeeded**.
   1. Si falla, devuelve un código de error detallado (ej. tarjeta rechazada).

De esta forma, la tienda puede cobrar dinero de forma segura sin construir toda la infraestructura financiera, externalizando el riesgo y la complejidad a la API de Stripe.


### PARTE PRACTICA (10 PUNTOS)

#### 1. Clonar el repositorio
git clone <URL_DE_TU_REPOSITORIO_FASTAPI>
cd <nombre-de-tu-repo-fastapi>

#### 2. Crear y activar el entorno virtual
python -m venv venv
#### Windows: .\venv\Scripts\activate
#### Linux/macOS: source venv/bin/activate

#### 3. Instalar dependencias (incluyendo pymongo y uvicorn)
pip install -r requirements.txt

#### Hacer los ajustes requeridos sobre el uso de mongodb u otra base de datos local o en la nube.

#### IMPORTANTE, FORMA DE EJECUCION:
#### Usar el estándar uvicorn <modulo>:<app_object>
uvicorn main:app --reload
