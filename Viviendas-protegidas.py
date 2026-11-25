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