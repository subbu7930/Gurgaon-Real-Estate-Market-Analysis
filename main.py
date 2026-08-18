import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')
# print(df.head())
# print(df.info())

# Data Cleaning
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(' ', '_')
      .str.replace(',', '')
)

print(df.columns.to_list())

# Numerical Column Cleaning
df['price'] = df['price'].astype(str).str.replace(",", "").astype(float)
print(df['price'])

df['area'] = df['area'].astype(str).str.replace(",", "").astype(int)
print(df['area'])

df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(",", "").astype(int)
print(df['rate_per_sqft'])

# Categorical Cleaning
df['status'] = df['status'].str.strip().str.lower()
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False})
print(df['rera_approval'])
df['flat_type'] = df['flat_type'].str.strip().str.lower()

df = df.drop_duplicates()
print(df)
print(df.info())

# 1) Which is thw costliest flat in the dataset?
costliest_flat = df.loc[df['price'].idxmax()]
print(costliest_flat)

# 2) Which locality has the highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
print(f"The locality with the highest average price is {highest_avg_price_locality}. ")

# 3) Which locality has the highest rate per square foot?
highest_rate_locality = df.groupby("locality")["rate_per_sqft"].mean().idxmax()
print(f"The locality with the highest rate per sqaure foot is {highest_rate_locality}. ")

# 4) Ready-to-move vs Under-construction pricing
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean() 
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()

if ready_to_move_avg_price>under_construction_avg_price:
    print("Ready-to-move properties cost more on average than under-construction properties.")

else:
    print("Under-construction properties cost more on average than ready-to move properties.")

# 5) Does RERA approval affect pricing?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()

if rera_approved_avg_price>rera_not_approved_avg_price:
    print("RERA approved properties command a price premium")

else:
    print("RERA approved properties do not command a price premium")

# 6) How does area impact price?
sns.scatterplot(data = df, x = 'area', y = 'price')
# plt.show()

#7) Which BHK configuration is most expensive?
most_expensive_bhk = df.groupby('bhk_count')['price'].mean().idxmax()
print(f"The most expensive BHK configuration on average is {most_expensive_bhk} BHK.")

# 8) Which property type is the costliest?
most_expensive_property_type = df.groupby('flat_type')['price'].mean().idxmax()
print(f"The most expenisve property type is {most_expensive_property_type}.")

# 9) Do certain builders price higher?
print(df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending=False).head(5))
# print the name of top 5
print("The top 5 builders that price higher are:")
top_5_builders = df.groupby("company_name")["rate_per_sqft"].mean().sort_values(ascending=False).head(5)
for builder in top_5_builders.index:
    print(builder, end =", " )

# 10) Are larger homes more expensive per sqft?
sns.scatterplot(data = df, x = 'area', y = 'rate_per_sqft')
plt.show()