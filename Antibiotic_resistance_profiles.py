#What do I want to know/see?

#- which clinically relevent antibiotics are my isolates resistant and susceptible to?
# -what resistance genes are in my isolates and what antibiotics/classes do they confer resistance to?


# red    - confirmed resistance
# orange - resistance gene present or intermediate confirmed resistance
# green  - confirmed susceptibility
# blue - unknown


#AMINOGLYCOSIDE
#
#BETA-LACTAM
#
#CEPHALOSPORIN
#
#DIAMINOPYRIMIDINE
#
#FLUOROQUINOLONE    O
#
#NITROFURAN         O
#
#SULFONAMIDE        O
#                   GL1    GL2     GL3     GL4     GL5     GL6     GL7     ,,,


import csv
import plotly.graph_objects as go


AntibioticClasses = {
        "aminoglycoside" : ["gentamicin"],
        "beta-lactam" : ["ampicillin"],
        "cephalosporin" : ["cefotaxime", "cefpodoxime", "cefalexin"],
        "diaminopyrimidine" : ["trimethoprim"],
        "fluoroquinolone" : ["ciprofloxacin"],
        "nitrofuran" : ["nitrofurantoin"],
        "sulfonamide" : ["sulfasoxazole", "sulfisoxazole"]}

AmrSTAR_set = {
        "GL3" : ["blaTEM-1A ampicillin", "sul2 sulfisozaxole"],
        "GL4" : ["blaTEM-1C ampicillin"],
        "GL6" : ["dfrA1 trimethoprim"],
        "GL7" : ["dfrA1 trimethoprim"],
        "GL8" : ["dfrA1 trimethoprim"],
        "GL9" : ["dfrA1 trimethoprim"],
        "GL10" : ["dfrA17 trimethoprim", "sul2 sulfisozaxole"],
        "GL11" : ["dfrA5 trimethoprim"],
        "GL12" : ["blaTEM-1B ampicillin", "dfrA1 trimethoprim", "sul1 sulfisoxazole"],
        "GL13" : ["blaTEM-1B ampicillin", "dfrA5 trimethoprim", "sul2 sulfisoxazole"],
        "GL14" : ["blaTEM-1B ampicillin", "dfrA17 trimethoprim", "sul1 sulfisoxazole"],
        "GL16" : ["blaTEM-1B ampicillin"],
        "GL18" : ["blaTEM-1A ampicillin", "sul1 sulfisoxazole"]
    }
AmrSTAR_by_class = {}

GL_sensitivity = {
    "GL1" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL2" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL3" : ['ampicillin R', 'cefpodoxime S', 'gentamicin R', 'nitrofurantoin R', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL4" : ['ampicillin R', 'cefpodoxime S', 'gentamicin I', 'nitrofurantoin R', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL5" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL6" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL7" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL8" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL9" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL10" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL11" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL12" : ['ampicillin R', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL13" : ['ampicillin R', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL14" : ['ampicillin R', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin R', 'trimethoprim R', 'cefalexin S', 'ciprofloxacin S'],
    "GL16" : ['ampicillin R', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL17" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL18" : ['ampicillin R', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S'],
    "GL20" : ['ampicillin S', 'cefpodoxime S', 'gentamicin S', 'nitrofurantoin S', 'trimethoprim S', 'cefalexin S', 'ciprofloxacin S']}

RGI_set = {}

def IdentifyClass(antibiotic):
    for Class, antibiotics in AntibioticClasses.items():
        if antibiotic in antibiotics:
            return Class

def Retrieve_RGI_dataset():

    """ Picks out the resistance genes confering resistance for each antibiotic class and stores in the dictionary RGI_set by isolate
    """

    RGIdata = open(r"C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\RGI_antibiotic_Rgenes.csv")
    CSV_RGIdata = csv.reader(RGIdata)

    for row in CSV_RGIdata:

        if len(row) != 0:

            Isolate_ID = row[0]
            RGI_set[Isolate_ID] = {}

            for AntibioticClass in AntibioticClasses.keys():
                RGI_set[Isolate_ID][AntibioticClass] = []


            for cell in row[1:]:

                if len(cell) == 0:
                    pass


                elif cell.startswith("Escherichia coli") or cell.startswith("Haemophilus influenzae"):
                    *header, AntibioticClass = cell.split(" ")

                    RGI_set[Isolate_ID][AntibioticClass.strip()].append(" ".join(header).strip())


                else:
                    if ";" in cell:
                        head, *tail = cell.split(";")
                        gene, tail2 = head.split()

                        RGI_set[Isolate_ID][tail2.strip()].append(gene.strip())

                        for AntibioticClass in tail:
                            RGI_set[Isolate_ID][AntibioticClass.strip()].append(gene.strip())
                        
                    else:
                        gene, AntibioticClass = cell.split()
                        RGI_set[Isolate_ID][AntibioticClass.strip()].append(gene.strip())

    RGIdata.close()

def StringGeneList_and_GeneCount():

    """ Creates the text string of resistance genes for each data point and provides the count of genes per antibiotic class.
    """

    GeneList = []
    GeneCount = []

    for isolate in GL_sensitivity.keys():

        #retrieve data from AmrSTAR_set and translates to the same format as RGI_set

        if isolate in AmrSTAR_set: #not all isolates have AmrSTAR data
            AmrSTAR_by_class[isolate] = {}
            for data in AmrSTAR_set[isolate]:
                gene, antibiotic = data.split()
                AmrSTAR_by_class[isolate][IdentifyClass(antibiotic)] = gene 
                #fortunately, the AmrSTAR set doesn't have multiple genes for a single antibiotic class
            
        # Picking out list of genes for each Antibiotic class in an isolate
        for AntibioticClass in AntibioticClasses.keys():
            #As the plot goes through my antibiotic class, so does all the for loops

            ClassGeneList = []
            ClassGeneCount = 0
            
            if len(RGI_set[isolate][AntibioticClass]) != 0: 
                for gene in RGI_set[isolate][AntibioticClass]:
                    ClassGeneList.append(gene)
                    ClassGeneCount += 1

            if isolate in AmrSTAR_by_class and AntibioticClass in AmrSTAR_by_class[isolate]:
                if AmrSTAR_by_class[isolate][AntibioticClass] not in ClassGeneList:
                    ClassGeneList.append(AmrSTAR_by_class[isolate][AntibioticClass]) 
                    ClassGeneCount += 1

            
            #Output
            GeneCount.append( (ClassGeneCount * 2) +10)

            if len(ClassGeneList) != 0:
                ClassGeneList.sort()
                GeneList.append('<br>'.join(ClassGeneList))
            
            else:
                GeneList.append("No resistance<br>genes detected")
            

    return GeneList, GeneCount

def ColourIdentifier():

    Colours = { "S" : 'rgb(44, 160, 101)',
                "I" : 'rgb(255, 144, 14)',
                "R" : 'rgb(255, 65, 54)',
                "U" : 'rgb(93, 164, 214)'}

    ColourList = []


    for isolate in GL_sensitivity.keys():

        #extract data from GL_sensitivity and structure by antibiotic class
        antibiotic_sensitivity_values = {}

        for antibiotic_sens in GL_sensitivity[isolate]:
            antibiotic, sensitivity = antibiotic_sens.split()
            antibiotic_sensitivity_values[IdentifyClass(antibiotic)] = sensitivity

        #Output            

        for AntibioticClass in AntibioticClasses.keys():

            if AntibioticClass in antibiotic_sensitivity_values:
                ColourList.append(Colours[antibiotic_sensitivity_values[AntibioticClass]])

            elif len(RGI_set[isolate][AntibioticClass]) != 0:
                ColourList.append(Colours['I'])
            
            elif isolate in AmrSTAR_by_class and AntibioticClass in AmrSTAR_by_class[isolate]:
                ColourList.append(Colours['I'])

            else:
                ColourList.append(Colours['U'])
    
    return ColourList

def PlotAntibioticData():

    #Preparing values for plot
    Genes, Count = StringGeneList_and_GeneCount()

    Colours = ColourIdentifier()

    # Antibiotic_sizes = []

    x = []
    y = []

    for X in range(1, len(RGI_set.keys()) + 1):
        for Y in range(1, len(AntibioticClasses.keys()) + 1):
            x.append(X), y.append(Y)

    #Plotting data
    fig = go.Figure(data=[go.Scatter(
        x=x, y=y,
        text = Genes,
        mode = 'markers',
        marker = dict(
            color = Colours,
            size = Count,
            sizemode ='area',
            sizeref = 2.*max(Count)/(60.**2),
            sizemin = 4

        )
    )])

    fig.update_layout(
        title = "Antibiotic Resistance Profiles - Resistant (red), Susceptible (green), Intermediate or known resistance genes (orange), Unknown (blue)",

        xaxis_title = "Isolate",
        xaxis = dict(
            tickmode = 'array',
            tickvals = [x for x in range(1, len(GL_sensitivity.keys()) + 1)],
            ticktext = [key for key in GL_sensitivity.keys()]
        ),
        yaxis_title = "Antibiotic Class",
        yaxis = dict(
            tickmode = 'array',
            tickvals = [x for x in range(1, len(AntibioticClasses.keys()) + 1)],
            ticktext = ["Aminoglycosides", "Beta-lactams", "Cephalosporins", "Diaminopyrimidines", "Fluoroquinolones", "Nitrofurans", "Sulfonamides"]
        )
    )

    fig.show()


if __name__ == "__main__":
    
    Retrieve_RGI_dataset()
    PlotAntibioticData()