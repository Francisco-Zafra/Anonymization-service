from generalization import *

df = pd.DataFrame({'Age': [25, 35, 20, 28, 40], 'Income': [50000, 80000, 60000, 70000, 90000]})
generalized_df = generalize_numeric_data(df, ['Age', 'Income'], 3)
print(generalized_df)