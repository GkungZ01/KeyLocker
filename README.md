# KeyLocker 1.0

A secure desktop application for managing and storing credentials with encryption.

## Features

- Secure credential storage with encryption
- Password-protected access
- Store multiple credentials with:
  - Name/Key identifier
  - Username/Email/Phone
  - Password
- Search functionality
- Copy username/password to clipboard
- Show/hide password toggle
- Add, edit, and delete credentials

## Security Features

- Encrypted storage using Fernet (symmetric encryption)
- Password-based key derivation using Scrypt
- Salted hashing
- Secure credential handling

## Requirements

- Python 3.x
- PyQt5
- cryptography
- pyperclip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/keylocker.git
cd keylocker
```

2. Install required packages:
```bash
pip install PyQt5 cryptography pyperclip
```

## Usage

1. Run the application:
```bash
python main.py
```

2. First time setup:
   - You'll be prompted to create a master password
   - This password will be required for future access

3. Managing credentials:
   - Click "Add" to create new entries
   - Select an entry to view/edit/delete
   - Use search to filter entries
   - Copy username/password using copy buttons
   - Toggle password visibility with "Show Password" checkbox

## Security Notes

- Your master password is never stored directly
- All credentials are encrypted before storage
- Data is stored locally in `mainpass.passlock`
- Always use a strong master password

## Development

The project structure:

```
keylocker/
├── main.py # Main application logic
├── ui/
│ ├── main.py # PyQt5 UI implementation
│ └── main.ui # Qt Designer UI file
├── components/
│ └── tkinterMore.py # Additional UI utilities
└── mainpass.passlock # Encrypted storage file
```

## License

[Add your chosen license here]

## Contributing

[Add contribution guidelines if accepting contributions]
=======
# KeyLocker
A program for storing passwords to prevent forgetting them.

Install Package
```
pip install cryptography PyQt5 pyperclip
```

Run Program
```
py main.py
```
>>>>>>> c5868a772c864604201e44564fde0bbafa8a21df
