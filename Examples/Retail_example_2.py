import numpy as np
import matplotlib.pyplot as plt

# Simulate sales data for two different pricing strategies
def simulate_sales(pricing_strategy, num_customers):
    if pricing_strategy == 'standard':
        # Simulate sales with standard pricing strategy
        return np.random.binomial(n=num_customers, p=0.05)  # 5% conversion rate
    elif pricing_strategy == 'discount':
        # Simulate sales with discount pricing strategy
        return np.random.binomial(n=num_customers, p=0.07)  # 7% conversion rate

# Number of customers in each group
total_customers = 1000

# Simulate sales for Group A (Standard Pricing) and Group B (Discount Pricing)
sales_standard = simulate_sales('standard', total_customers)
sales_discount = simulate_sales('discount', total_customers)

# Calculate total sales for each group
total_sales_standard = np.sum(sales_standard)
total_sales_discount = np.sum(sales_discount)

# Plotting the results
labels = ['Standard Pricing', 'Discount Pricing']
sales_data = [total_sales_standard, total_sales_discount]

plt.bar(labels, sales_data, color=['blue', 'green'])
plt.xlabel('Pricing Strategy')
plt.ylabel('Total Sales')
plt.title('Retail A/B Test: Total Sales Comparison')
plt.show()

# Compare the results and determine the winner
if total_sales_standard > total_sales_discount:
    print("Standard Pricing strategy generated more sales.")
elif total_sales_standard < total_sales_discount:
    print("Discount Pricing strategy generated more sales.")
else:
    print("Both pricing strategies generated equal sales.")