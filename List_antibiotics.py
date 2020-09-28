import csv
from os import path, remove

def ListAntibiotics():

    RGIdata = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Data\RGIdata.csv")
    CSV_data = csv.reader(RGIdata)

    if path.exists(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\AntibioticsSelection.txt"):
        remove(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\AntibioticsSelection.txt")

    Output = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\AntibioticsSelection.txt", "a+")

    antibiotics = []

    for row in CSV_data:

        for cell in row[1:]:

            UnsortedList = []

            if len(cell) == 0:
                pass

            elif ";" in cell:
                head, *tail = cell.split(";")

                *_, tail2 = head.strip().split()

                UnsortedList.append(tail2.strip())

                for antibiotic in tail:
                    UnsortedList.append(antibiotic.strip())
                    
            elif cell.startswith("Escherichia") or cell.startswith("Haemophilus"):

                *_, tail1, tail2 = cell.strip().split()
                UnsortedList.append(tail1.strip()), UnsortedList.append(tail2.strip())

            else:
                _, tail = cell.split()

                UnsortedList.append(tail.strip())


            for antibiotic in UnsortedList:
                if antibiotic not in antibiotics:
                    antibiotics.append(antibiotic)

    antibiotics.sort()

    Output.write("All antibiotics which a resistance gene was detected to confer resistance for from all isolates:\n")

    for antibiotic in antibiotics:
        Output.write(antibiotic + "\n")

    Output.close()
    RGIdata.close()


if __name__ == "__main__":
    ListAntibiotics()