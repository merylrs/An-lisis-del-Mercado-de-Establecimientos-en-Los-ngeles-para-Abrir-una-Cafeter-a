#!/usr/bin/env python
# coding: utf-8

# # Análisis del Mercado de Establecimientos en Los Ángeles para Abrir una Cafetería

# ## Descripción del Proyecto: <a id='intro'></a>
# 
# Este proyecto tiene como objetivo realizar un análisis detallado del mercado de restaurantes en Los Ángeles, con el propósito de ofrecer información clave a potenciales inversionistas. A través de la exploración de datos exhaustivos de establecimientos, examinaremos las proporciones de diferentes tipos de restaurantes, la presencia de cadenas, la relación entre estas y el número de asientos, así como el análisis de ubicaciones más destacadas. La finalidad última es llegar a conclusiones sólidas y proporcionar recomendaciones estratégicas para aquellos interesados en invertir en la próspera escena gastronómica de Los Ángeles.
# 
# ### Contenido
# 
# 1. [Introducción](#introduction): Contextualización del proyecto y objetivos del análisis de mercado.
# 2. [Descarga y Preparación de Datos](#p1): Descarga de datos y preparación.
# 3. [Análisis de Datos](#p2): Exploración y análisis de los datos ya preparados.
# 4. [Conclusiones y Recomendaciones](#conclusiones): Síntesis de hallazgos clave y recomendaciones estratégicas.
# 5. [Enlace a la Presentación](#presentacion_link): Inclusión del enlace a la presentación final en formato PDF.
# 

# ## Descarga y Preparación de Datos <a id='#p1'></a>

# ### Bibliotecas

# In[2]:


# Importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats


# ### Carga de Datos

# In[107]:


ruta = "/datasets/rest_data_us.csv"
data = pd.read_csv(ruta)


# In[108]:


# Mostrar las primeras filas 
data.head()


# Vemos registros detallados de diversos establecimientos en Los Ángeles. Cada columna incluye información como el nombre del establecimiento, su dirección, si pertenece a una cadena, el tipo de establecimiento (cafetería, restaurante, comida rápida, etc.) y el número de asientos disponibles. Estos datos constituyen la base para nuestro análisis de mercado

# In[109]:


data.info()


# In[110]:


# Verificar valores ausentes 
data.isnull().sum()


# Al ser solo 3 filas, elegimos llenar esos valores nulos con "No especificado" en lugar de eliminarlas para no perder la otra información.

# In[111]:


# Sustituir valores nulos con "No especificado"
data['chain'].fillna('No especificado', inplace=True)


# In[112]:


data.isnull().sum()


# In[113]:


# Verificar duplicados 
data.duplicated().sum()


# Vemos que a este punto nuestros datos no tienen valores ausentes ni duplicados. Podemos avanzar.

# ## Análisis de Datos <a id='#p2'></a>

# ### Proporciones de Establecimientos

# In[114]:


# Proporciones de tipos de establecimientos
type_proportions = data['object_type'].value_counts(normalize=True)

# Graficar las proporciones
plt.figure(figsize=(10, 6))
sns.barplot(x=type_proportions.index, y=type_proportions.values, palette="viridis")
plt.title('Proporciones de Tipos de Establecimientos')
plt.xlabel('Tipo de Establecimiento')
plt.ylabel('Proporción')
plt.xticks(rotation=45, ha="right")
plt.show()


# Al analizar el gráfico de proporciones de tipos de establecimientos, se observa una clara predominancia de la categoría 'Restaurant', la cual se encuentra significativamente por encima de las demás categorías. En particular, 'Fast Food' muestra una proporción notablemente más baja, seguida por otras categorías que exhiben una presencia aún menor. Este patrón revela una fuerte presencia de restaurantes en comparación con otros tipos de establecimientos, destacando la relevancia y popularidad de esta categoría en el mercado de Los Ángeles.

# ### Proporciones de Establecimientos que Pertenecen a Cadenas

# In[115]:


# Proporciones de establecimientos que pertenecen a una cadena
chain_proportions = data['chain'].value_counts(normalize=True)

# Graficar las proporciones
plt.figure(figsize=(8, 6))
sns.barplot(x=chain_proportions.index, y=chain_proportions.values, palette="pastel")
plt.title('Proporciones de Establecimientos que Pertenecen a una Cadena')
plt.xlabel('Pertenece a una Cadena')
plt.ylabel('Proporción')
plt.show()


# Vemos que hay más establecimientos que no perteneceen a una cadena, pero veamos de cuántos restaurantes lo hacen o no.
# 

# In[116]:


# Contar la cantidad de restaurantes que pertenecen o no a una cadena
chain_counts = data['chain'].value_counts()

# Graficar la cantidad de restaurantes que pertenecen o no a una cadena
plt.figure(figsize=(8, 6))
sns.barplot(x=chain_counts.index, y=chain_counts.values, palette="pastel")
plt.title('Cantidad de Restaurantes que Pertenecen o no a una Cadena')
plt.xlabel('Pertenece a una Cadena')
plt.ylabel('Número de Restaurantes')
plt.show()


# Vemos en el caso de Restaurantes también son parte de la tendencia.

# ### Proporción de Establecimientos en Una Cadena

# In[117]:


# Proporción de cada tipo de establecimiento que pertenece a una cadena
chain_proportion_by_type = data.groupby('object_type')['chain'].value_counts(normalize=True).unstack().fillna(0)

# Graficar la proporción de cada tipo de establecimiento que pertenece a una cadena
plt.figure(figsize=(12, 6))
sns.barplot(x=chain_proportion_by_type.index, y=chain_proportion_by_type[True], palette='coolwarm')
plt.title('Proporción de Establecimientos que Pertenecen a una Cadena por Tipo')
plt.xlabel('Tipo de Establecimiento')
plt.ylabel('Proporción que Pertenecen a una Cadena')
plt.xticks(rotation=45, ha="right")
plt.show()


# Vemos que los tipos de establecimientos más comunes que pertenecen a una cadena son Bakery, Cafe, Fast Food y Pizza. Estos muestran proporciones más altas de pertenencia a cadenas en comparación con Restaurant y Bar, que tienen proporciones más bajas. Esta información sugiere que ciertos sectores, como Bakery y Cafe, tienden a adoptar el modelo de cadena con mayor frecuencia, posiblemente debido a factores como la estandarización de productos y servicios. 

# ### Qué Determina a una Cadena

# In[118]:


# Boxplot del número de asientos para establecimientos que pertenecen o no a una cadena
plt.figure(figsize=(10, 6))
sns.boxplot(x='chain', y='number', data=data, palette='husl')
plt.title('Distribución del Número de Asientos para Establecimientos que Pertenecen o no a una Cadena')
plt.xlabel('Pertenece a una Cadena')
plt.ylabel('Número de Asientos')
plt.show()


# - Los establecimientos que **no** pertenecen a una cadena tienen un rango de asientos que va aproximadamente de 50 a 150.
# - Los establecimientos que pertenecen a una cadena tienen un rango de asientos que va aproximadamente de 100 a 200. Esto sugiere que estos establecimientos tienden a ser más grandes.
# - Los establecimientos donde no se especifica si pertenecen a una cadena o no, el rango de asientos va aproximadamente de 0 a 50.

# Según el gráfico, los establecimientos que pertenecen a una cadena tienden a tener un mayor número de asientos, con un rango que va aproximadamente de 100 a 200. Esto podría sugerir que las cadenas se caracterizan por tener unos pocos establecimientos con un montón de asientos.

# ### Promedio de Número de Asientos Para Cada Establecimiento

# In[119]:


# Promedio de número de asientos por tipo de establecimiento
average_seats_by_type = data.groupby('object_type')['number'].mean().sort_values(ascending=False)

# Graficar el promedio de número de asientos por tipo de establecimiento
plt.figure(figsize=(12, 6))
sns.barplot(x=average_seats_by_type.index, y=average_seats_by_type.values, palette='viridis')
plt.title('Promedio de Número de Asientos por Tipo de Establecimiento')
plt.xlabel('Tipo de Establecimiento')
plt.ylabel('Promedio de Número de Asientos')
plt.xticks(rotation=45, ha="right")
plt.show()


# El tipo de restaurante que tiene el mayor número promedio de asientos es el "Restaurante".
# 
# - **Restaurante**: Este tipo de establecimiento tiene el mayor número promedio de asientos, lo que indica que los restaurantes suelen ser más grandes y pueden acomodar a más clientes.
# - **Bar**: Los bares tienen el segundo mayor número promedio de asientos, lo que sugiere que también pueden acomodar a un buen número de clientes, aunque no tanto como los restaurantes.
# - **Fast Food, Pizza, Café, Bakery**: Estos tipos de establecimientos tienen un número promedio de asientos más bajo, lo que podría indicar que son más pequeños o que su modelo de negocio no requiere tantos asientos.

# ### Separación de Columna 'address'

# In[120]:


# Extraer nombres de calles de la columna "address"
data['street'] = data['address'].str.split().str[1:].apply(lambda x: ' '.join(x))

# Mostrar las primeras filas del DataFrame con la nueva columna "street"
data[['address', 'street']].head()


# ### Top 10 de las Mejores Calles

# In[121]:


# Obtener las diez mejores calles por número de establecimientos
top_10_streets = data['street'].value_counts().nlargest(10)

# Graficar las diez mejores calles por número de restaurantes
plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_streets.index, y=top_10_streets.values, palette='muted')
plt.title('Las Diez Mejores Calles por Número de Establecimientos')
plt.xlabel('Calle')
plt.ylabel('Número de Establecimientos')
plt.xticks(rotation=45, ha="right")
plt.show()


# Podemos ver que:
# 
# - **W. Sunset Blvd** tiene la mayor cantidad de establecimientos con casi 300 establecimientos.
# - **S. Western Ave** tiene la menor cantidad de establecimientos entre las diez calles presentadas, con poco más de 100 establecimientos.
# - Las demás calles presentadas en el gráfico tienen un número de establecimientos que varía entre 150 para abajo.

# ### Número de Calles Con Un Solo Establecimiento

# In[122]:


# Contar el número de calles con un solo establecimiento
calles_con_un_establecimiento = data['street'].value_counts()[data['street'].value_counts() == 1].count()

# Mostrar el resultado
print(f"Número de calles que solo tienen un establecimiento: {calles_con_un_establecimiento}")


# Descubrimos que es un número significativo de calles con un solo establecimiento.

# ### Distribución del Número de Asientos (en calles con muchos establecimientos)

# Para mejor legibilidad, explayaremos esta distribución únicamente en el Top 10 de las calles con muchos establecimientos.

# In[123]:


# Gráfico de barras apiladas con las calles seleccionadas para todos los tipos de establecimientos
plt.figure(figsize=(15, 8))
sns.countplot(x='street', hue='seat_range', data=filtered_busy_streets_data, palette='coolwarm', dodge=False)
plt.title('Distribución del Número de Asientos en Calles con Muchos Establecimientos (Top 10)')
plt.xlabel('Calle')
plt.ylabel('Número de Establecimientos')
plt.xticks(rotation=45, ha="right")
plt.legend(title='Número de Asientos', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# De este gráfico de barras que muestra la distribución del número de asientos en las calles con muchos establecimientos, podemos observar las siguientes tendencias:
# 
# - La mayoría de los establecimientos en estas calles tienen entre **250 y 300 asientos**. Esto podría indicar que estos restaurantes están diseñados para acomodar a un gran número de clientes.
# - El número de restaurantes con entre **450 y 500 asientos** es el más bajo. Esto podría sugerir que los restaurantes de este tamaño son menos comunes, tal vez debido a las limitaciones de espacio o a la preferencia de los propietarios de restaurantes por establecimientos más pequeños.
# - El número de restaurantes con entre **150-200 asientos** y **350-400 asientos** es casi el mismo. Esto podría indicar una distribución uniforme de restaurantes de estos tamaños en estas calles.

# ## Conclusiones y Recomendaciones <a id='#conclusiones'></a>

# 1. **Conclusiones:**
#    - El análisis del mercado de restaurantes en Los Ángeles revela un escenario prometedor para la introducción de un pequeño café con atención de robots. Aunque los restaurantes y la comida rápida dominan el mercado, la posición de las cafeterías, especialmente una con un enfoque innovador, como la atención de robots, presenta una oportunidad única.
# 
#    - La proporción de cafeterías, aunque actualmente en tercer lugar, destaca la capacidad del café con robots para diferenciarse en un mercado saturado. La novedad de la atención robotizada ofrece una ventaja competitiva y atraerá a un público interesado en experiencias únicas.
# 
#    - La posición de las cafeterías como establecimientos más pequeños en comparación con restaurantes y comida rápida también sugiere una mayor flexibilidad operativa y la posibilidad de adaptarse rápidamente a las tendencias del mercado.
# 
# 2. **Recomendaciones:**
#    - Los Ángeles ofrece un mercado diverso y receptivo a propuestas innovadoras. Una cafetería con atención de robots puede captar la atención y generar interés, aprovechando la demanda de experiencias únicas.
# 
#    - Enfocarse en la experiencia del cliente. Crear un ambiente acogedor y agradable, complementado con la eficiencia de la atención robotizada, podría ser un factor diferenciador clave y contribuir al éxito continuo del café.
# 
#    - Consideramos estratégico explorar la posibilidad de desarrollar una cadena de estos cafés. La expansión a múltiples ubicaciones podría maximizar el impacto de la propuesta única y ofrecer una mayor visibilidad en el mercado.
# 

# ## Enlace a La Presentación <a id='#presentacion_link'></a>

# [Presentation](https://drive.google.com/file/d/1aeHU6WaYoNbbfrIVCADk9Gyc3o_ASF38/view?usp=sharing)
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




