import pandas as pd
import random
from faker import Faker
import streamlit as st
from io import BytesIO

fake = Faker()

# ---------------------
# STREAMLIT CONFIG
# ---------------------
st.set_page_config(
    page_title="🌿 John Deere Quality Data Formatter",
    layout="wide"
)

st.title("🌿 John Deere Quality Management Data Formatter")
st.write("Simulates Deere manufacturing data, cleans it, and generates formatted reports.")

# ---------------------
# MOCK DATA GENERATOR
# ---------------------
def generate_mock_data(num_records=200):
    products = [
        "X350 Lawn Tractor", "S780 Combine", "8600 Forage Harvester",
        "332G Skid Steer", "310SL Backhoe Loader", "944K Wheel Loader"
    ]

    factories = [
        "Davenport Works", "Harvester Works", "Waterloo Works",
        "Des Moines Works", "East Moline Works"
    ]

    shifts = ["Morning", "Afternoon", "Night"]

    data = []
    for i in range(num_records):
        batch_id = f"JD-BATCH-{2025}-{1000+i}"
        product = random.choice(products)
        factory_location = random.choice(factories)
        production_date = fake.date_between(start_date='-30d', end_date='today')
        units_produced = random.randint(500, 1500)
        defective_units = random.randint(0, int(units_produced * 0.08))
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

    # Sort ascending by default for consistency in output
    df.sort_values(by="Production Date", ascending=True, inplace=True)
    return df

# ---------------------
# EXPORT TO EXCEL
# ---------------------
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Quality Report")

        workbook = writer.book
        worksheet = writer.sheets["Quality Report"]

        # Deere-style header formatting
        header_format = workbook.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#006400",
            "font_color": "white",
            "border": 1
        })

        # Apply header styling
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Format defect rate column as percentage
        defect_col_index = df.columns.get_loc("Defect Rate (%)")
        percent_format = workbook.add_format({"num_format": "0.00%", "border": 1})
        worksheet.set_column(defect_col_index, defect_col_index, 15, percent_format)

        # Fix "Production Date" column width & formatting to avoid #####
        date_col_index = df.columns.get_loc("Production Date")
        date_format = workbook.add_format({"num_format": "yyyy-mm-dd", "border": 1})
        worksheet.set_column(date_col_index, date_col_index, 20, date_format)

        # Right-align numeric columns with thousand separators
        numeric_format = workbook.add_format({"align": "right", "num_format": "#,##0", "border": 1})
        for col_name in ["Units Produced", "Defective Units"]:
            col_idx = df.columns.get_loc(col_name)
            worksheet.set_column(col_idx, col_idx, 15, numeric_format)

        # Auto-size remaining columns for better readability
        for idx, col in enumerate(df.columns):
            if idx not in [defect_col_index, date_col_index]:
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(idx, idx, max_len)

        # Freeze header row for easier scrolling
        worksheet.freeze_panes(1, 0)

    output.seek(0)
    return output

# ---------------------
# APP UI
# ---------------------
st.sidebar.header("⚙️ Settings")
num_records = st.sidebar.slider("Number of records", 50, 500, 200, 50)

if st.sidebar.button("Generate Mock Data"):
    df = generate_mock_data(num_records)
    st.success(f"✅ Generated {num_records} rows of Deere manufacturing data!")

    st.subheader("📄 Preview of Generated Data")

    # Force ascending sort in preview
    df_preview = df.sort_values(by="Production Date", ascending=True).reset_index(drop=True)
    st.dataframe(df_preview)

    # CSV download (sorted ascending)
    csv = df_preview.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="john_deere_quality_data.csv",
        mime="text/csv"
    )

    # Excel download (sorted ascending)
    excel = to_excel(df_preview)
    st.download_button(
        label="⬇️ Download Excel",
        data=excel,
        file_name="john_deere_quality_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👈 Use the sidebar to generate mock data and download reports.")
