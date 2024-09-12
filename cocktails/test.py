import pandas as pd


def clean_text(text):
    if isinstance(text, str):
        return text.strip().replace('\n', ' ')
    return text


def parse_excel_column(file_path, sheet_name=0, column_index=14):
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    column_data = df.iloc[:, column_index - 1]

    filtered_data = column_data.dropna()

    cleaned_data = filtered_data.apply(clean_text)

    unique_data = cleaned_data.drop_duplicates()

    return unique_data.tolist()


def write_to_txt(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in data:
            file.write(f"{line}\n")


file_path = 'book.xlsx'
output_file = 'tools.txt'
data = parse_excel_column(file_path)
print(data)
# write_to_txt(data, output_file)
# print(f"Данные записаны в файл {output_file}")