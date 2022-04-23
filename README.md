
# 🔎 Search Engine
![web-gui](https://user-images.githubusercontent.com/56369636/164840888-06f9b8df-eae9-4376-b77d-8e7cc5868eb8.png)


## 🔗 What it Does
Using a corpus of over 55,000 web pages, we built a fully-functioning search engine that returns results in less than 300ms. There are two main steps to our search engine: indexing and searching. Indexing is run as a preprocessing step which basically creates a lookup table that stores all of the unique tokens (words) found in the corpus, along with which page they were found on and a weight associated with how important/relevant each word was to the page. The main event is, of course, the searching, which is exactly what it sounds like! Just simply type your query in the search bar, and it will scour our index on all 55,000 pages to deliver you the best results. There are two ways to view the searching: in the terminal or on the web GUI. Both are functionally the same! Feel free to check out [our presentation](https://docs.google.com/presentation/d/1jLecR7rZEYygrGMsuFzDREkn6NhVuYlr4yLZYbKTqCA/edit?usp=sharing) on it as well to learn more details about the indexing and searching!

## ⚙️ Tech Stack
We used **Python** for all of the logic for both indexing and searching. For the web GUI, we used a Jinja **HTML** template styled with some custom **CSS** that hit our **Flask** server for queries.

## 🚧 Challenges
This was our first time building a search engine and our greatest challenges were reducing our query time and balancing memory usage. When building the index, it's not scalable to store the entire index in memory, so we had to carefully balance our writes to disk. But writing the partial indices to disk posed another problem: merging. We had to find a way to efficiently merge them without running in the same problem of excessive memory usage. We lastly had to employ several techniques, such as indexing our index and converting bottleneck Python functions to Cython, as our initial search times were several orders of magnitude more than our final 300ms threshold.

## 🔧 How to Run

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
