## Takes in list of journals and citations and outputs weighted network links
## Written for "Contaminants in Waterways" technical analysis and data visualization

import csv

# Global variables and data structures
journals = {}
categories = {}
citations = {}
total_journals = 0

# Read in list of distinct journals and initialize their category to "other"
def getJournals():
    global journals,total_journals
    with open('network/distinctJournals.csv', 'r') as csvfile:
        data = csv.reader(csvfile)
        for d in data:
            journals[d[0].lower()] = "other"
            total_journals +=1

# Read in categories of interest which must appear in order of priority
def getCategories():
    global categories
    with open('categories/categoryList.csv', 'r') as csvfile:
        data = csv.DictReader(csvfile)
        for d in data:
            categories[d["category"]] = {"count":0,"area":d["subjectArea"],"name":d["fullName"]}

# Iterate over each category of interest and categorize all journals
def categorizeJournals():
    global categories,journals,total_journals
    for category in categories.keys():
        with open("categories/" + str(category)+'.csv', 'r') as csvfile:
            data = csv.DictReader(csvfile, delimiter=";")
            categorized = 0
            for d in data:
                if d["Title"].lower() in journals.keys() and journals[d["Title"].lower()] == "other":
                    journals[d["Title"].lower()] = category
                    categories[category]["count"] += 1
                    categorized += 1

    # Journals that remain uncategorized are grouped as "Other"
    categories["other"] = {"count":total_journals-categorized,"area":"Other","name":"Journals that do not fall under any category of interest"}

# Categorize citations according to their journals' categories
def categorizeCitations():
    global journals,citations
    with open('network/citations.csv', 'r') as csvfile:
        data = csv.DictReader(csvfile)

        # If A cited B, this will be encoded as 'from' A 'to' B
        for d in data:
            from_category = journals[d["source"].lower()]
            to_category = journals[d["journal"].lower()]

            # Keep track of citation weights
            if (from_category,to_category) in citations.keys():
                citations[(from_category,to_category)] += 1
            else:
                citations[(from_category,to_category)] = 1

# Format element data as csv for Kumu data visualization
def outputElements():
    global categories
    with open('kumu/KumuElements.csv', 'w') as csvfile:
        csvfile.write("Label,Journals,Type,Description\n")
        for category in categories.keys():
            c = categories[category]
            output = [category,c["count"],c["area"],str(c["area"])+": "+str(c["name"])]

            # Kumu element format is Label,Journals,Type,Description
            csvfile.write('"{}",{},"{}","{}"\n'.format(category,c["count"],c["area"],str(c["area"])+": "+str(c["name"])))

# Format link data as csv for Kumu data visualization
def outputLinks():
    global citations
    with open('kumu/KumuLinks.csv', 'w') as csvfile:
        for citation in citations.keys():

            # Kumu link format is csv From,To,Weight
            csvfile.write(str(citation[0]) + "," + str(citation[1]) + "," + str(citations[citation])+"\n")

# Driver code
getJournals()
getCategories()
categorizeJournals()
categorizeCitations()
outputElements()
outputLinks()
