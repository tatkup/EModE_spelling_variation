import os
import re
import xml.etree.ElementTree as ET

def contains_invalid_characters(text):
    invalid_characters = r'[∣¶¦•.,?!:;/()\[\]▪❧{}⟨⟩_〈…〉●]'
    return re.search(invalid_characters, text) is not None

def process_xml_file(input_file, output_file):
    print(f"Processing {input_file}")
    # Check if the input file is empty
    if os.path.getsize(input_file) == 0:
        print(f"Skipped {input_file}. The file is empty.")
        return

    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Find all 'w' tags, exclude tags with pos="ab", pos="crd", lemma="n/a", and containing invalid characters
    output_lines = []
    for w_tag in root.findall('.//{http://www.tei-c.org/ns/1.0}w'):
        reg_value = w_tag.get('reg')
        value = w_tag.text

        if value and not contains_invalid_characters(value):
            if reg_value:
                output_lines.append(f'{reg_value},{value}')
            else:
                output_lines.append(f'{value},{value}')

    # Ensure the output directory exists
    output_directory = os.path.dirname(output_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Write the output to a file in the same subfolder as the input file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write('\r\n'.join(output_lines))  # Use appropriate newline character
    print(f"Processed {input_file}. Output saved to {output_file}")

def process_all_files_in_directory(input_directory):
    # Traverse all files in the input directory and its subdirectories
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.xml'):  # Process only XML files
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, file.replace('.xml', '_aligned.txt'))
                process_xml_file(input_file, output_file)

# Replace 'C:/Users/aphri/Desktop/processed' with the path to your input directory
input_directory = 'E:/EarlyPrint/Abel Jeffes'
process_all_files_in_directory(input_directory)
