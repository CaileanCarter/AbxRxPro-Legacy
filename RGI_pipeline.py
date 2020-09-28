#Workflow for the retrieval of information from TSV RGI files and picking relevent data
#to be inputted into the Antibiotic_resistance_profiles.py

import Merge_TSV_files
import Get_resGenes
import List_antibiotics
from os import path, remove

if path.exists(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv"):
    remove(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv")

Merge_TSV_files.DeleteBin()
Merge_TSV_files.Extract_RGI_data()
List_antibiotics.ListAntibiotics()
Get_resGenes.Retrieve_resGenes()


