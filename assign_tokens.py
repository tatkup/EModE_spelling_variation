import os
import csv

def is_valid_token(token):
    # Check if the token contains any digits or '&'
    return not any(char.isdigit() or char == '&' for char in token)

def create_new_csv(csv_file, output_csv):
    types_and_tokens = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                token, token_type = row
                # Lowercase each character in the token and token_type
                token = token.lower()
                token_type = token_type.lower()
                if is_valid_token(token):
                    if token_type in types_and_tokens:
                        types_and_tokens[token_type].append(token)
                    else:
                        types_and_tokens[token_type] = [token]

    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for token_type, tokens in types_and_tokens.items():
            # Lowercase each token before writing to the output file
            tokens = [token.lower() for token in tokens]
            writer.writerow([token_type] + tokens)

def process_csv_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                input_csv = os.path.join(root, file)
                output_folder = os.path.join(root, "tok")
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                output_csv = os.path.join(output_folder, file.replace('.csv', '_tok.txt'))

                print(f"Processing: {input_csv} -> {output_csv}")

                create_new_csv(input_csv, output_csv)

                print(f"Finished processing: {input_csv}")

# Example usage
directory = 'E:/EarlyPrint/printers_FINAL/printer_entropy'
process_csv_files(directory)

print("Finished.")
