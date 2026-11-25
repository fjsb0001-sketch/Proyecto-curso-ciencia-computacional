import pandas as pd

# 1. Cargar el dataset
df = pd.read_csv('journalist.csv')

# 2. Dimensiones generales y valores nulos
print("=== 1. DIMENSIONES GENERALES ===")
print(f"Número de filas: {df.shape[0]}")
print(f"Número de columnas: {df.shape[1]}")

print("\nValores nulos por columna:")
nulos = df.isnull().sum()
print(nulos[nulos > 0])

# 3. Resumen de variables cuantitativas (numéricas)
print("\n=== 2. VARIABLES CUANTITATIVAS ===")
num_cols = df.select_dtypes(include=['number']).columns
resumen_num = pd.DataFrame({
    'Promedio (Media)': df[num_cols].mean(),
    'Mediana': df[num_cols].median(),
    'Mínimo': df[num_cols].min(),
    'Máximo': df[num_cols].max(),
    'Desviación estándar': df[num_cols].std()
})
print(resumen_num.round(2))

# 4. Resumen de variables cualitativas (categóricas)
print("\n=== 3. VARIABLES CUALITATIVAS ===")
cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
resumen_cat = []

for col in cat_cols:
    no_nulos = df[col].count()
    moda = df[col].mode()[0]
    frecuencia = df[col].value_counts().iloc[0]
    porcentaje = (frecuencia / no_nulos) * 100
    
    resumen_cat.append({
        'Variable': col,
        'Categorías únicas': df[col].nunique(),
        'Valor más frecuente (Moda)': moda,
        'Frecuencia': frecuencia,
        '% sobre no nulos': round(porcentaje, 1)
    })

df_resumen_cat = pd.DataFrame(resumen_cat).set_index('Variable')
print(df_resumen_cat)

# 5. Visualización exploratoria de los datos
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle('Análisis Exploratorio de Vivienda Protegida en España (journalist.csv)', fontsize=16, fontweight='bold', y=0.98)

# Gráfico 1: Evolución anual del total de viviendas ('value' agrupado por 'year')
viviendas_por_anio = df.groupby('year')['value'].sum()
axes[0, 0].plot(viviendas_por_anio.index, viviendas_por_anio.values, color='#1f77b4', linewidth=2.2)
axes[0, 0].fill_between(viviendas_por_anio.index, viviendas_por_anio.values, color='#1f77b4', alpha=0.15)
axes[0, 0].set_title('Evolución anual del total de viviendas protegidas', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Año')
axes[0, 0].set_ylabel('Total de viviendas')

# Gráfico 2: Top 10 Comunidades Autónomas por número de registros
top_ccaa = df['ccaa'].value_counts().head(10)
sns.barplot(x=top_ccaa.values, y=top_ccaa.index, ax=axes[0, 1], palette='viridis')
axes[0, 1].set_title('Top 10 Comunidades Autónomas (por nº de registros)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Número de registros')
axes[0, 1].set_ylabel('')

# Gráfico 3: Distribución según el tipo de promotor
promotores = df['promotor'].value_counts()
sns.barplot(x=promotores.index, y=promotores.values, ax=axes[1, 0], palette='Set2')
axes[1, 0].set_title('Registros por tipo de promotor', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Tipo de promotor')
axes[1, 0].set_ylabel('Número de registros')
axes[1, 0].tick_params(axis='x', rotation=15)

# Gráfico 4: Distribución de 'value' (escala logarítmica para apreciar valores extremos)
sns.histplot(df[df['value'] > 0]['value'], bins=35, log_scale=True, ax=axes[1, 1], color='#ff7f0e', kde=True)
axes[1, 1].set_title('Distribución de viviendas por registro (escala logarítmica)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Número de viviendas (escala log)')
axes[1, 1].set_ylabel('Frecuencia')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('analisis_exploratorio.png', dpi=300)
plt.show()
