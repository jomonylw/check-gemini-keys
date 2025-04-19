# Gemini API Key Checker

This is a Python script for checking the validity of Gemini API keys. It verifies the keys by sending simple requests to the Gemini API and saves the valid keys to	an output file.

[中文版本](README.zh-CN.md)

## Introduction

This tool is designed to help users quickly validate multiple Gemini API keys. It reads an input file containing API keys, tests each key individually, and writes the valid keys to an output file. The tool uses a low-cost, fast-responding model `gemini-1.5-flash-latest` for testing to minimize resource consumption.

## Installation

1. Ensure you have Python 3 installed.
2. Install the required dependency:

   ```bash
   pip install requests
   ```

   Or use the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a text file named `gemini_key.txt` and list the Gemini API keys you want to test, one per line.
2. Run the script:

   ```bash
   python check_gemini_keys.py
   ```

3. The script will check each key and display the results in the console. Valid keys will be saved to `valid_key.txt`.

## Configuration Options

The script includes the following configuration options, which you can modify in the `check_gemini_keys.py` file as needed:

- **INPUT_FILENAME**: Input file name, defaults to `gemini_key.txt`.
- **OUTPUT_FILENAME**: Output file name, defaults to `valid_key.txt`.
- **MODEL_NAME**: Model name used for testing, defaults to `gemini-1.5-flash-latest`.
- **REQUEST_TIMEOUT**: Request timeout in seconds, defaults to 10 seconds.
- **DELAY_BETWEEN_REQUESTS**: Delay between requests in seconds, defaults to 0.5 seconds, to prevent rate limiting.

## Output Information

During execution, the script outputs the following information:

- The status of each key check, including whether it is valid and any specific error messages (if applicable).
- A summary upon completion, showing the number of valid keys found out of the total checked.
- Valid keys are written to the specified output file.

## Notes

- Ensure that the Gemini API is enabled and you have the necessary permissions before running the script.
- If you encounter rate limiting issues, try increasing the `DELAY_BETWEEN_REQUESTS` value.
- The script uses ANSI color codes in the console to display different types of messages (green for valid, red for errors, yellow for warnings).

## License

This project is licensed under the MIT License. See the `LICENSE` file (if available) for details.