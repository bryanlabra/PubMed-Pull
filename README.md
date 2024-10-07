# PubMed-Pull
This repository contains a script that takes in a name, or list of names, of authors and pulls a list of their publications from PubMed for analysis in VOSviewer

- **Very Helpful Links:**
  - VOSviewer download [https://www.waveshare.com/wiki/1.14inch_LCD_Module](https://www.vosviewer.com/download)

## Step 1: Clone Repository
  Open your code editor within the target folder and type:
   ```bash
   git clone https://github.com/bryanlabra/VOSviewer-PubMed_Citations.git
   ```

## Step 2: Create and activate a virtual environment 

   ```bash
   python3 -m venv .venv
   ```
  activate the virtual environment ".venv"
  
   ```bash
   source ./.venv/bin/activate  
   ```
  
## Step 3: update system to have required libaries

   ```bash
   pip install -r requirements.txt
   ```

## Step 4: run script from command line

   ```bash
   python ./src/pubmed-pull.py ./citations/ "Authors Name" latest-30
   ```





