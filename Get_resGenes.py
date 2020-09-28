import csv
from os import remove, path

def Retrieve_resGenes():
    
    RGIdata = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGIdata.csv")
    CSV_RGIdata = csv.reader(RGIdata)


    if path.exists(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv"):
        remove(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv")

    Output = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv", "a+")
    OutputToCSV = csv.writer(Output)

    AntibioticClasses = ["aminoglycoside", "gentamicin",
            "beta-lactam", "ampicillin",
            "cephalosporin", "cefotaxime", "cefpodoxime", "cefalexin",
            "diaminopyrimidine", "trimethoprim",
            "fluoroquinolone", "ciprofloxacin",
            "nitrofuran", "nitrofurantoin",
            "sulfonamide", "sulfasoxazole", "sulfisoxazole"]

    for row in CSV_RGIdata:

        if len(row[0:1]) != 0:

            SortingList = [row[0]] #first cell is isolate name

            for cell in row[1:]:

                NewCell = ""
                    
                if ";" in cell:
                    
                    head, *tail = cell.split(";")
                    *head2, tail2 = head.strip().split()

                    gene = " ".join(head2)

                    if tail2.strip() in AntibioticClasses:
                        NewCell += " ".join([gene, tail2])

                    elif any([lambda x: x.strip() in AntibioticClasses, tail]):

                        for item in tail:
                            if item.strip() in AntibioticClasses:

                                if NewCell.startswith(gene):
                                    NewCell += "; " + item.strip()
                                
                                else:
                                    NewCell += " ".join([gene, item.strip()])


                elif cell.startswith("Escherichia") or cell.startswith("Haemophilus"):

                    *head, tail1, tail2 = cell.strip().split()

                    gene = " ".join(head)

                    if tail1 in AntibioticClasses:
                        NewCell += " ".join([gene, tail1])

                    if tail2 in AntibioticClasses:

                        if gene in NewCell:
                            NewCell += "; " + tail2.strip()
                        else:
                            NewCell += " ".join([gene, tail2.strip()])


                elif len(cell) != 0:
                    _, tail = cell.split()

                    if tail.strip() in AntibioticClasses:
                        SortingList.append(cell)

                
                if len(NewCell) != 0:
                    SortingList.append(NewCell)

            OutputToCSV.writerow(item for item in SortingList)


    RGIdata.close()
    Output.close()
