import pandas as pd
import warnings
import json


def json_to_excel():
    with open("gmbs_data.json", 'r') as file:
        data = json.load(file)
        print(len(data))

    # Sort entries alphabetically
    data = sorted(data, key=lambda d: d["name"])

    # Entries with telephone
    entries_with_telephone = [obj for obj in data if obj["telephone"] != "Unknown"]

    # Entries without telephone
    entries_without_telephone = [obj for obj in data if obj["telephone"] == "Unknown"]

    # Append [with telephone] and [without telephone]
    data = entries_with_telephone + entries_without_telephone

    # Convert list to pandas DataFrame
    data = pd.DataFrame(data)

    writer = pd.ExcelWriter('google_maps_business.xlsx')
    data.to_excel(writer, sheet_name="google maps business", index=False, na_rep='Nan')

    for index, column in enumerate(data):
        column_width = max(data[column].astype(str).map(len).max(), len(column))
        col_idx = data.columns.get_loc(column)
        writer.sheets['google maps business'].set_column(col_idx, col_idx, column_width)

    warnings.filterwarnings("ignore")
    writer.save()


if __name__ == "__main__":
    json_to_excel()

