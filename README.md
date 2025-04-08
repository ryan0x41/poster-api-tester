# poster-api-tester

Simple Python blackbox integration tester for Poster API.
## Requirements

- Python 3.8+
- pip

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/ryan0x41/poster-api-tester.git
cd poster-api-tester
```

2. **Create a virtual environment (recommended)**

```bash
python3 -m venv venv source venv/bin/activate # windows is different
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Place a placeholder image**

Put a small image named `temp_profile.png` in the project folder for image upload tests.

## Usage

Run in one of the following modes:

- `get`: Tests read-only endpoints.
- `set`: Tests write/update endpoints (creates and deletes test data).
- `ep`: Tests equivalence partitioning on appropriate endpoints.
- `bva`: Tests boundary value analysis on appropriate endpoints.

```bash
python automated.py get
python automated.py set
python automated.py ep
python automated.py bva
```

## Notes

- Tests will fail if the API is offline or test data is missing.    
- `set` mode will register and delete a test user automatically.

---

MIT License  
© 2025 Ryan Sheridan
