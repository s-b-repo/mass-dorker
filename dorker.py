import requests
import urllib.parse

def load_dorks(file_path):
    """Load dorks from a file, each dork on a new line."""
    try:
        with open(file_path, 'r') as file:
            dorks = [line.strip() for line in file if line.strip()]
        return dorks
    except FileNotFoundError:
        print("Dork file not found.")
        return []

def google_dork_search(query):
    """Perform a Google search with the dork query."""
    base_url = "https://www.google.com/search?q="
    search_url = base_url + urllib.parse.quote(query)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            return response.text  # Return the HTML of the page
        else:
            print(f"Failed to retrieve results for query: {query}")
            return None
    except Exception as e:
        print(f"Error during request: {e}")
        return None

def run_dorks(keyword, dork_file="dorks.txt", output_file="results.txt"):
    """Run each dork from the file with the provided keyword and save results."""
    dorks = load_dorks(dork_file)
    results = {}

    with open(output_file, 'w') as file:
        for dork in dorks:
            dork_query = dork.format(keyword)
            print(f"Searching with dork: {dork_query}")
            result = google_dork_search(dork_query)
            if result:
                # Save the first 500 characters of the result for brevity
                results[dork_query] = result[:500]
                file.write(f"Query: {dork_query}\nResult:\n{result[:500]}\n{'-' * 40}\n")
            else:
                results[dork_query] = "No results found or failed to retrieve."
                file.write(f"Query: {dork_query}\nResult: No results found or failed to retrieve.\n{'-' * 40}\n")
    
    print(f"All results saved to {output_file}")
    return results

# Keyword to search for
keyword = "sample_keyword"

# Run the dorks and save results to results.txt
results = run_dorks(keyword)
