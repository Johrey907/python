import pandas as pd

# Input data
data = {
    'memberid': ['mowen', 'ray', 'phile', 'sheila', 'martha'],
    'savings': [1000000, 1300000, 700000, 1000000, 900000],
    'loanno': [4, 2, 5, 0, 3],
    'loantaken': [800000, 500000, 1300000, 0, 2000000],
    'interest': [80000, 50000, 130000, 0, 200000],
    'latepay': [1, 0, 2, 0, 1],
    'fines': [15000, 5000, 40000, 5000, 10000]
}

df = pd.DataFrame(data)

# Total profit pool
total_interest = df['interest'].sum()
total_fine = df['fines'].sum()
total_profit = total_interest + total_fine

# Weights
w_savings = 3       # 30%
w_interest = 5      # 50%
w_loans_taken = 1     # 10%
w_late = -1           # -10% (penalty)

# Calculate individual scores
df['Score'] = (
    df['savings'] * w_savings +
    df['interest'] * w_interest +
    df['loantaken'] * w_loans_taken +
    df['latepay'] * w_late
)

# Normalize scores to distribute profit
total_score = df['Score'].sum()
df['ProfitShare'] = (df['Score'] / total_score) * total_profit if total_score != 0 else 0

# Calculate percentile rank (0-100)
df['pct_rank'] = df['Score'].rank(pct=True, method='max') * 100

# Assign credit grades based on percentile
def assign_grade(p):
    if p >= 70:
        return 'A'
    elif p >= 40:
        return 'B'
    else:
        return 'C'

df['credit_grade'] = df['pct_rank'].apply(assign_grade)

# Final output
final_result = df[['memberid', 'savings', 'loanno', 'loantaken', 'interest', 'latepay', 'fines', 'Score', 'ProfitShare', 'pct_rank', 'credit_grade']]
print(final_result)

# Save to CSV
final_result.to_csv('save_squad_final.csv', index=False)

print("CSV file saved: save_squad_final.csv")
