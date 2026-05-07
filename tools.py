"""
    Phase 2 - Search Tools for the Prompt Designer Agent
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In this file you will create three search tools that the agent
    can use to find information:
      1. DuckDuckGo  — general web search  (free, no API key)
      2. ArXiv       — academic papers      (free, no API key)
      3. PubMed      — biomedical papers    (free, no API key)

    Each tool returns a list of SearchResult objects defined in models.py.
"""


# TODO:
# Phase 2 — Imports
#
# > Import the SearchResult model from models.py
# Reference: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
#
# > Import xml.etree.ElementTree as ET for parsing ArXiv XML responses
# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
#
# > Import urllib.request and urllib.parse for making HTTP requests to ArXiv and PubMed
# Reference: https://docs.python.org/3/library/urllib.request.html
# Reference: https://docs.python.org/3/library/urllib.parse.html
#
# > Import json for parsing PubMed JSON responses
# Reference: https://docs.python.org/3/library/json.html
#
# > Use a try/except block to import DDGS from duckduckgo_search
#   Set a flag HAS_DUCKDUCKGO = True if successful, False if ImportError
# Reference: https://pypi.org/project/duckduckgo-search/
# Reference: https://docs.python.org/3/tutorial/errors.html#handling-exceptions
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 1 — Create the DuckDuckGoSearchTool class
#
# > Create a class called DuckDuckGoSearchTool
# Reference: https://docs.python.org/3/tutorial/classes.html
#
# > Inside the class, create an __init__ method that takes max_results (int)
#   with a default value of 5, and stores it as self.max_results
# Reference: https://docs.python.org/3/tutorial/classes.html#class-objects
#
# > Inside the class, create a method called search that takes query (str) as
#   a parameter and returns a list[SearchResult]
# Reference: https://pypi.org/project/duckduckgo-search/
#
# > Inside the search method, check if HAS_DUCKDUCKGO is False. If so, print
#   a warning and return self._mock_search(query) as a fallback
#
# > Inside the search method, use a try/except block. In the try block:
#   - Create a DDGS() instance using a with statement
#   - Call ddgs.text(query, max_results=self.max_results) to get results
#   - For each result r, create a SearchResult with:
#     title=r.get('title', 'No title')
#     url=r.get('href', r.get('link', ''))
#     snippet=r.get('body', r.get('snippet', ''))
#     source="web"
#   - Return the list of SearchResult objects
#   In the except block, print the error and return self._mock_search(query)
# Reference: https://pypi.org/project/duckduckgo-search/
# Reference: https://docs.python.org/3/tutorial/errors.html#handling-exceptions
#
# > Inside the class, create a method called _mock_search that takes query (str)
#   and returns a list of 2 mock SearchResult objects for testing without the package
# Reference: https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Create the ArxivSearchTool class
#
# > Create a class called ArxivSearchTool
# Reference: https://docs.python.org/3/tutorial/classes.html
#
# > Inside the class, create an __init__ method that takes max_results (int)
#   with a default of 5, and stores it as self.max_results
#   Also store the ArXiv API base URL as self.base_url = "http://export.arxiv.org/api/query"
# Reference: https://info.arxiv.org/help/api/basics.html
#
# > Inside the class, create a method called search that takes query (str)
#   and returns a list[SearchResult]
#
# > Inside the search method, use a try/except block. In the try block:
#   - Build the API URL parameters using urllib.parse.urlencode with:
#     search_query=f"all:{query}", start=0, max_results=self.max_results
#   - Construct the full url: f"{self.base_url}?{params}"
#   - Use urllib.request.urlopen(url) to fetch the response, then .read().decode('utf-8')
#   - Parse the XML response using ET.fromstring(response_text)
#   - Define the Atom namespace: ns = {'atom': 'http://www.w3.org/2005/Atom'}
#   - Find all 'atom:entry' elements using root.findall('atom:entry', ns)
#   - For each entry, extract:
#     title = entry.find('atom:title', ns).text.strip()
#     url   = entry.find('atom:id', ns).text.strip()
#     snippet = first 300 chars of entry.find('atom:summary', ns).text.strip()
#   - Create a SearchResult with source="arxiv" and append to results
#   - Return the results list
#   In the except block, print the error and return an empty list
# Reference: https://info.arxiv.org/help/api/basics.html
# Reference: https://docs.python.org/3/library/xml.etree.elementtree.html
# Reference: https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen
# Reference: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 3 — Create the PubMedSearchTool class
#
# > Create a class called PubMedSearchTool
# Reference: https://docs.python.org/3/tutorial/classes.html
#
# > Inside the class, create an __init__ method that takes max_results (int)
#   with a default of 5, and stores it as self.max_results
#   Also store two base URLs:
#     self.search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     self.summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
# Reference: https://www.ncbi.nlm.nih.gov/books/NBK25501/
#
# > Inside the class, create a method called search that takes query (str)
#   and returns a list[SearchResult]
#
# > Inside the search method, use a try/except block. In the try block:
#   Step A — Search for PubMed IDs:
#   - Build search params using urllib.parse.urlencode with:
#     db="pubmed", term=query, retmax=self.max_results, retmode="json"
#   - Fetch the response from f"{self.search_url}?{params}" using urllib.request.urlopen
#   - Parse the JSON with json.loads(response_text)
#   - Extract the list of IDs: data['esearchresult']['idlist']
#   - If no IDs found, return an empty list
#
#   Step B — Fetch summaries for the IDs:
#   - Build summary params with:
#     db="pubmed", id=",".join(id_list), retmode="json"
#   - Fetch the response from f"{self.summary_url}?{params}"
#   - Parse the JSON and access data['result']
#   - For each pmid in id_list, get the article info from result[pmid]
#   - Create a SearchResult with:
#     title = article.get('title', 'No title')
#     url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
#     snippet = first 300 chars of article.get('sorttitle', article.get('title', ''))
#     source = "pubmed"
#   - Return the results list
#
#   In the except block, print the error and return an empty list
# Reference: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
# Reference: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESummary
# Reference: https://docs.python.org/3/library/json.html#json.loads
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 4 — Create the format_results helper function
#
# > Create a function called format_results that takes results (list[SearchResult])
#   as a parameter and returns a formatted string
# Reference: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
#
# > Inside the function, if results is empty, return "No search results found."
#
# > Inside the function, iterate over the results with enumerate(results, 1)
#   For each result, create a formatted entry:
#     f"[{i}] {result.title}\n    Source: {result.source}\n    URL: {result.url}\n    {result.snippet}\n"
# Reference: https://docs.python.org/3/library/functions.html#enumerate
#
# > Return the joined formatted entries separated by newlines
# Reference: https://docs.python.org/3/library/stdtypes.html#str.join
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 5 — Create the get_search_tools factory function
#
# > Create a function called get_search_tools that takes max_results (int) with
#   a default of 5 and returns a dictionary mapping tool names to tool instances
# Reference: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
#
# > Inside the function, return a dict with keys "web", "arxiv", "pubmed"
#   mapped to instances of DuckDuckGoSearchTool, ArxivSearchTool, PubMedSearchTool
#   each initialized with max_results
# Reference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE
