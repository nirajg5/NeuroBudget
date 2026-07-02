from tools.csv_parser import CSVParser

FILE_PATH = "uploads/raw/transactions.csv"

df = CSVParser.read_csv(FILE_PATH)

print()

print("Shape")

print(CSVParser.get_shape(df))

print()

print("Columns")

print(CSVParser.get_columns(df))

print()

print("Preview")

print(CSVParser.preview(df))

print()

print("Info")

print(CSVParser.dataframe_info(df))