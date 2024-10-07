import os
import requests
import argparse
import time

def fetch_pubmed_citations(save_directory, name="", selection="latest-10"):
    # Define PubMed retrieval type (defaulted to "medline" for plain-text PubMed format)
    rettype = "medline"

    # Define number of results based on selection
    if selection == "latest-10":
        retmax = 10
    elif selection == "latest-30":
        retmax = 30
    else:
        raise ValueError("Invalid selection option. Use 'latest-10' or 'latest-30'.")

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # PubMed search URL with query; using the [AU] field tag to restrict to authors
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": f"{name}[AU]",  # Restrict search to authors
        "retmode": "json",
        "retmax": retmax,
        "sort": "most+recent"  # Get the most recent articles
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Retry mechanism for API requests
    for attempt in range(3):
        try:
            search_response = requests.get(base_url, params=search_params, headers=headers)
            search_response.raise_for_status()  # Raise an error for non-200 status codes

            try:
                search_data = search_response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Received invalid JSON response from PubMed API.")
                return

            pmids = search_data.get("esearchresult", {}).get("idlist", [])
            if not pmids:
                print("No results found.")
                return

            # Join PMIDs for citation retrieval
            pmid_list = ",".join(pmids)
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": pmid_list,
                "retmode": "text",
                "rettype": rettype
            }

            # Fetch citations in the requested format
            citation_response = requests.get(fetch_url, params=fetch_params, headers=headers)
            citation_response.raise_for_status()  # Ensure successful response

            # Filter out only the fields needed by VOSviewer
            fields_to_keep = {"PMID", "FAU", "AU", "AD", "MH"}
            filtered_lines = []
            for line in citation_response.text.splitlines():
                # Check if the line starts with one of the specified fields
                if any(line.startswith(field) for field in fields_to_keep):
                    filtered_lines.append(line)

            # Save filtered citations to a file
            file_name = f"{name.replace(' ', '_')}_pubmed_citations.txt"
            file_path = os.path.join(save_directory, file_name)
            with open(file_path, "w") as file:
                file.write("\n".join(filtered_lines))
            print(f"Citations saved to {file_path}")
            break  # Exit loop if successful

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying

    else:
        print("Error: Failed to fetch citations after 3 attempts.")
        return

# CLI argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PubMed citations for a given author's name.")
    parser.add_argument("save_directory", type=str, help="Directory to save the citation file")
    parser.add_argument("name", type=str, help="Name of the professor or search term")
    parser.add_argument("selection", type=str, choices=["latest-10", "latest-30"], help="Fetch the latest 10 or 30 results")

    args = parser.parse_args()
    fetch_pubmed_citations(args.save_directory, args.name, args.selection)