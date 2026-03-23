import pandas as pd

# Read the unicorn CSV file we created manually
unicorns = pd.read_csv("unicorns.csv")

# Print all unicorns
print("All Unicorns:")
print(unicorns)

# Print only Indian unicorns
print("\nIndian Unicorns:")
print(unicorns[unicorns["country"] == "India"])

# Print only US unicorns
print("\nUS Unicorns:")
print(unicorns[unicorns["country"] == "USA"])

# Print dataset size
print("\nDataset size:", unicorns.shape)

