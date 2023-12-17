import os
import requests
from multiprocessing import Pool, Manager

# Define a function for downloading and saving each page
def download_and_save(pid):
    if os.path.exists(f"data/{pid}.html"):
        return pid
    url = f"https://abstracts.societyforscience.org/Home/FullAbstract?ProjectId={pid}"
    page = requests.get(url)
    if page.status_code == 200:
        with open(f"data/{pid}.html", "w") as f:
            f.write(page.text)
    else:
        print(f"Error: {pid}")
    return pid

# Main function to handle multiprocessing
def main(pids, num_processes):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create a pool of worker processes
    with Pool(num_processes) as pool:
        # Map the range of project IDs to the download function
        results = pool.map(download_and_save, pids)

    assert len(results) == len(pids)
    assert len(os.listdir("data")) == len(pids)

# Parameters for multiprocessing
num_processes = 10  # Adjust this based on your system's capability
pids = open("pids.txt").read().splitlines()

# Run the main function
if __name__ == '__main__':
    main(pids, num_processes)
