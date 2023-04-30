from generalization import *

df = pd.DataFrame({'Age': [25, 35, 20, 28, 40], 'Income': [50000, 80000, 60000, 70000, 90000], 'Country':['United States', 'Spain', 'China', 'Costa Rica', 'Australia']})
#generalized_df = generalize_numeric_data(df, ['Age', 'Income'], 3)
generalized_df = generalize_categorical_data(df, ['Country'], ['country'])
print(generalized_df)

