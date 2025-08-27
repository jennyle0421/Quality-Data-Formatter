import pandas as pd
from pathlib import Path

# Paths
DATA_PATH = Path("john_deere_quality_data.csv")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def format_data():
    # Read the generated mock data
    df = pd.read_csv(DATA_PATH)

    # Sort by production date (latest first)
    df["Production Date"] = pd.to_datetime(df["Production Date"])
    df.sort_values(by="Production Date", ascending=False, inplace=True)

    # Recalculate defect rate to ensure accuracy
    df["Defect Rate (%)"] = (
        df["Defective Units"] / df["Units Produced"] * 100
    ).round(2)

    # Save cleaned CSV
    clean_csv_path = REPORTS_DIR / "clean_quality_report.csv"
    df.to_csv(clean_csv_path, index=False)

    # Save formatted Excel report
    excel_path = REPORTS_DIR / "clean_quality_report.xlsx"
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Quality Report", index=False)

        # Add professional Deere-style formatting
        workbook = writer.book
        worksheet = writer.sheets["Quality Report"]

        # Format headers
        header_format = workbook.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#006400",   # Deere dark green
            "font_color": "white",
            "border": 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Format defect rate column to always show %
        percent_format = workbook.add_format({"num_format": "0.00%", "border": 1})
        defect_col_index = df.columns.get_loc("Defect Rate (%)")
        worksheet.set_column(defect_col_index, defect_col_index, 15, percent_format)

    print(f"✅ Reports generated!\n- CSV: {clean_csv_path}\n- Excel: {excel_path}")

if __name__ == "__main__":
    format_data()
