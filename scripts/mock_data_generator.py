import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_mock_data(num_records=200):
    data = []

    # Deere-style product names
    products = [
        "X350 Lawn Tractor", "S780 Combine", "8600 Forage Harvester",
        "332G Skid Steer", "310SL Backhoe Loader", "944K Wheel Loader"
    ]

    # Deere factory locations
    factories = [
        "Davenport Works", "Harvester Works", "Waterloo Works",
        "Des Moines Works", "East Moline Works"
    ]

    shifts = ["Morning", "Afternoon", "Night"]

    for i in range(num_records):
        batch_id = f"JD-BATCH-{2025}-{1000+i}"
        product = random.choice(products)
        factory_location = random.choice(factories)
        production_date = fake.date_between(start_date='-30d', end_date='today')
        units_produced = random.randint(500, 1500)
        defective_units = random.randint(0, int(units_produced * 0.08))  # max 8% defect rate
        defect_rate = round((defective_units / units_produced) * 100, 2)
        operator = fake.name()
        shift = random.choice(shifts)

        data.append([
            batch_id, product, factory_location, production_date,
            units_produced, defective_units, defect_rate, operator, shift
        ])

    df = pd.DataFrame(data, columns=[
        "Batch ID", "Product Name", "Factory Location", "Production Date",
        "Units Produced", "Defective Units", "Defect Rate (%)",
        "Operator Name", "Shift"
    ])

    return df

if __name__ == "__main__":
    df = generate_mock_data(200)
    df.to_csv("john_deere_quality_data.csv", index=False)
    print("✅ Mock John Deere manufacturing data saved to 'john_deere_quality_data.csv'")
