#Retrieves all the data from the TSV files exported from IRIDA and merges to a CSV file
#Only taking the genes ID and what antibiotic/class it confers resistance to


import csv
from os import listdir, remove, path


def Extract_RGI_data():

    #Create a list of TSV files
    ListedFiles = listdir(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGI_analysis")

    #location to store all the RGI data
    dataStore = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGIdata.csv", "a+")
    RgiData = csv.writer(dataStore)

    for RGI_file in ListedFiles:
        file = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGI_analysis\{}".format(RGI_file))
        RGI_data = csv.reader(file, delimiter="\t")


        data = [RGI_file[9:13].replace("-", "")]

        for row in RGI_data:
            if row[0] != "ORF_ID" and len(row[0]) != 0:
                data.append("{gene} {antibiotics}".format(gene = row[8], antibiotics = row[14].replace(" antibiotics", "").replace(" antibiotic", "")))
                # print(row[8] + row[14])

        RgiData.writerow(item for item in data)
        
        file.close()
    
    dataStore.close()
   
def DeleteBin():
    if path.exists(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGIdata.csv"):
        remove(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGIdata.csv")


if __name__ == "__main__":
    
    Extract_RGI_data()

   