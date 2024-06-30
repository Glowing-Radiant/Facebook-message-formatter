import sys
import os
from bs4 import BeautifulSoup
from datetime import datetime

def parse_html_to_txt(input_file, output_file):
    try:
        print(f"Reading file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        print("Parsing HTML content")
        soup = BeautifulSoup(content, 'html.parser')

        messages = []
        for div in soup.find_all('div', class_='pam _3-95 _2pi0 _2lej uiBoxWhite noborder'):
            sender = div.find('div', class_='_3-96 _2pio _2lek _2lel').text.strip()
            message = div.find('div', class_='_3-96 _2let').text.strip()
            timestamp = div.find('div', class_='_3-94 _2lem').text.strip()

            # Convert timestamp to datetime object for sorting
            date_obj = datetime.strptime(timestamp, '%d %b %Y, %H:%M')
            messages.append((sender, message, date_obj))

        print(f"Found {len(messages)} messages")

        print("Sorting messages")
        messages.sort(key=lambda x: x[2])  # Sort by timestamp

        print(f"Writing to output file: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as file:
            for sender, message, timestamp in messages:
                file.write(f"{sender}, {message}, {timestamp.strftime('%d %b %Y, %H:%M')}\n")

        print("Conversion complete")
        return True
    except Exception as e:
        print(f"Error processing file {input_file}: {str(e)}")
        return False

def batch_convert(parent_directory):
    print(f"Starting batch conversion in: {parent_directory}")
    successful = 0
    failed = 0
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file == "message_1.html":
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, "formatted_messages.txt")
                print(f"Converting: {input_file}")
                if parse_html_to_txt(input_file, output_file):
                    successful += 1
                else:
                    failed += 1
    print(f"Batch conversion complete. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("For single file: python script.py input_file.html output_file.txt")
        print("For batch processing: python script.py --batch parent_directory")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) != 3:
            print("Usage for batch processing: python script.py --batch parent_directory")
            sys.exit(1)
        parent_directory = sys.argv[2]
        batch_convert(parent_directory)
    else:
        if len(sys.argv) != 3:
            print("Usage for single file: python script.py input_file.html output_file.txt")
            sys.exit(1)
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        parse_html_to_txt(input_file, output_file)
