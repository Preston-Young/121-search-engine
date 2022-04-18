
# Search Engine

## How to run:

1. **Prerequisites**
    -   macOS 10.15+ / Linux
    -   gcc>=9, clang >= 10 (C++17 code)
    -   Properly set CC and CXX environment variables
    -   Python 3.9
    
2. **Setup**
     - Virtual Environment and External Packages
        -   Create venv
    	   	 - `python3 -m venv /path/to/new/virtual/environment`
        -   Activate your virtual environment
    	   	 -   See here for platform specific command: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)
        -   Install packages:
    	   	 -   `pip install -r requirements.txt`
	 - Compile Cython file
        -   Compile cython_helpers.pyx
    	   	 -   `python c_setup.py build_ext --inplace`
 	 
	 - Index directories
        -   Create the following directories in project root
    	   	 -   index
    	   	 -   index_of_index
    	   	 -   index_storage

3. **Running Index (This should take around 98 minutes)**
	 - Run index file
		 - `python index.py`

4. **Running Search Engine**
	-   Terminal GUI
		-   `python search.py`
	-   Web GUI
		-   `export FLASK_APP=gui`
		-   `export FLASK_ENV=development`
		-   `python gui.py`
		-   Look at terminal and navigate to http://127.0.0.1:[PORT] with the port that flask created the web app on
