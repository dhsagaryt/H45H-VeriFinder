
# H45H Verifinder

## Overview

H45H Verifinder is a versatile tool for file integrity verification. It calculates hash values for files using multiple algorithms and compares these computed hashes with a provided hash value to verify file authenticity. If no hash value is provided, the tool will display the computed hash values for the file.
## Features

- Multi-Algorithm Hash Calculation: Computes file hashes using MD5, SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 algorithms.
- Hash Verification: Compares a provided hash value against computed hash values to verify the file's integrity.
- Detailed Reporting: Provides detailed reports on hash verification results, showing both provided and computed hashes.
- Rich Text Output: (If rich module is installed) Displays results with styled text and tables for a more readable output.
- Basic Output Mode: Provides a plain text output if the rich module is not installed.
- Cross-Platform Compatibility: Available as executables for Windows, Linux, and macOS, and can be run from source on any platform with Python.


## Usage / Output

 ## DIRECT USE WITHOUT INSTALL
 YOU CAN DIRECT USE SCRIPT FILE WITHOUT INSTALL ANY DEPENDENCIES [H45H-VeriFinder-v3.8.py](H45H-VeriFinder-v3.8.py) OR YOU CAN USE DIRECT EXECUTABLE FILE [H45H-VeriFinder-v3.8.exe](dist/)
 
 ## Usage

    1. Launch the tool.
    2. Enter the file path of the file you wish to verify.
    3. Optionally, enter a hash value to verify. If left empty, the tool will display computed hash values for the file.

 ## Output

    - Rich Mode:
      Displays styled text and tables if rich is installed.

    - Basic Mode: 
      Shows plain text output if rich is not available.

- Example
```javascript
Enter the file path: example_file.txt
Enter the hash value to verify or (Leave empty):
```

## Installation (if need)

 - Pre-built Executables: 
   
    A pre-built executable for Windows (.exe) is available in the releases section. Download the executable for your platform and run it directly.

 - From Source:
 
    To run the tool from source, follow these steps:
 
    ### [1] Clone the Repository:

     ```bash
     git clone https://github.com/yourusername/H45H-Verifinder.git
     cd H45H-Verifinder
     ```
    ### [2] Install Dependencies: 
   
     The tool requires the rich module for styled output. Install it using:
     
     ```bash
     pip install rich
     ```

     If rich is not installed, the program will run in basic mode with plain text output.

    ### [3] Run the Tool:
     Execute the script with:
    
     ```bash
     python your_script.py
     ```


## Contributing

Contributions are welcome! 

Please fork the repository and submit a pull request. For major changes, open an issue to discuss the changes before submitting a pull request.
## License

This project is licensed under the MIT License - see the [License](LICENSE) file for details.
## Contact to Developer

- [@dhsagaryt](https://www.instagram.com/dhsagaryt/)

