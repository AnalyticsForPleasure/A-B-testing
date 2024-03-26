import numpy as np
import matplotlib.pyplot as plt


# **************************************************************************************************************
# In this example:
# We have a control group (Version A) and a variation group (Version B).
# Both groups represent the time spent on the landing page, but Version B is expected to have higher engagement due to changes made.
# We generate simulated data for both groups using normal distributions with different means but the same standard deviation.
# By plotting the distributions, we can visualize the differences between the control and variation groups.
# The plot will show two histograms representing the time spent on the landing page for both groups. It will help us compare the distributions of the control and variation groups. If the variation group consistently shows higher values compared to the control group, it suggests that the changes made in Version B might be effective in increasing user engagement.
#
# Having the control group allows us to isolate the impact of the changes in Version B and determine whether they lead to a significant improvement compared to the original version (Version A).
# ***************************************************************************************************************

# Simulated data for time spent on the landing page
np.random.seed(42)  # for reproducibility
control_group = np.random.normal(loc=60, scale=10, size=1000)  # Control group (Version A)
variation_group = np.random.normal(loc=65, scale=10, size=1000)  # Variation group (Version B)

# Plotting the distributions
plt.figure(figsize=(10, 6))
plt.hist(control_group, bins=30, alpha=0.5, label='Control Group (Version A)')
plt.hist(variation_group, bins=30, alpha=0.5, label='Variation Group (Version B)')
plt.xlabel('Time Spent on Landing Page (seconds)')
plt.ylabel('Frequency')
plt.title('Distribution of Time Spent on Landing Page')
plt.legend()
plt.show()