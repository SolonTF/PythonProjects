# Python Practice Projects for Aspiring Data Scientist in Pharma & Health  
This repository is a collection of small Python projects, data science notebooks and learning exercises tailored for someone looking to build a career in pharmaceutical or healthcare data science, or even to spin up entrepreneurial analytics ideas. It focuses on practical skills like pulling real‑world datasets, cleaning and analysing data, and visualising results.  

## Structure  
- **/scripts/** — self‑contained Python scripts covering data acquisition, API integration and exploratory analysis  
- **/data/** — example CSV datasets used in the scripts and notebooks  
- **/notebooks/** — Jupyter notebooks demonstrating in‑depth analysis and exploratory workflows  
- **/docs/** — explanatory write‑ups and summaries of projects, including interpretation of results  

## Example Topics  

Self-learning (Python):
- Data visualisation with Matplotlib to communicate study results  
- Basic web scraping and API access (e.g. Crossref) to retrieve biomedical research articles

Research assistant training for MATLAB (UCL):
- Chaos Game algorithms — generating fractals with iterative rules
- Monte Carlo simulation — π estimation and stochastic modelling
- Logistic map experiments — chaos, bifurcations and dynamical systems 

### Crossref API Script  
The `scripts/crossref_api.py` file fetches open‑access metadata from the Crossref API. You can run it to fetch open‑access metadata for a query term (e.g. "ageing biomarkers" or "drug repurposing"), save the results to a CSV and generate a quick publication‑year distribution chart. This can help you explore research trends, identify prolific journals and inspire new project ideas.  

To execute the script:  

```bash
python scripts/crossref_api.py
```  

You will be prompted to enter a search query. The script will then contact the Crossref API, collect articles related to your keyword, and output a CSV file and a simple plot.  

## Contribution & Extension Ideas  
- Add notebooks showing deeper analysis of the Crossref output (e.g. co‑author networks or topic modelling)  
- Incorporate other public datasets relevant to pharma and health (clinical trial databases, adverse event reports, etc.)  
- Experiment with interactive dashboards (Streamlit or Dash) to present findings in a business‑friendly way, useful for entrepreneurial pitches  

Feel free to fork and adapt these projects to your own interests. Contributions that expand the scope towards other areas of data science or healthcare entrepreneurship are always welcome.
