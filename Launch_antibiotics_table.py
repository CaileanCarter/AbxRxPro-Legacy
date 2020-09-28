import plotly.graph_objects as go 

AntibioticClasses = {
        "Aminoglycosides" : ["gentamicin"],
        "Beta-lactams" : ["ampicillin"],
        "Cephalosporins" : ["cefotaxime", "cefpodoxime", "cefalexin"],
        "Diaminopyrimidines" : ["trimethoprim"],
        "Fluoroquinolones" : ["ciprofloxacin"],
        "Nitrofurans" : ["nitrofurantoin"],
        "Sulfonamides" : ["sulfasoxazole", "sulfisoxazole"]}

Antibiotics_clinically_used = [
                            "Ampicillin",
                            "Cefalexin",
                            "Cefpodoxime",
                            "Ciprofloxacin",
                            "Co-amoxiclav",
                            "Gentamicin",
                            "Nitrofurantoin",
                            "Trimethoprim"
                            ]


def Sort_AntibioticClasses():

    Antibiotic_classes = []

    for Class, antibiotics in AntibioticClasses.items():
        text = "{Class} ({antibiotics})".format(Class=Class, antibiotics=", ".join(antibiotics))
        Antibiotic_classes.append(text)

    return Antibiotic_classes


def Retrieve_detected_antibiotics():

    Antibiotics_detected = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\AntibioticsSelection.txt", "r")

    Detected_list = []

    for antibiotic in Antibiotics_detected:
        if not antibiotic.startswith("All"):
            Detected_list.append(antibiotic.strip())

    Antibiotics_detected.close()
    return Detected_list


def LaunchTable():

    Sorted_antibiotic_classes = Sort_AntibioticClasses()
    Antibiotics_detected = Retrieve_detected_antibiotics()
    
    fig = go.Figure(data=[go.Table(
                    header=dict(values=["Antibiotics Used at NNUH", "Classes (antibiotics) plotted", "All Antibiotics Detected"]),
                    cells=dict(values=[Antibiotics_clinically_used, Sorted_antibiotic_classes, Antibiotics_detected])
    )])

    fig.show()


if __name__ == "__main__":
    LaunchTable()