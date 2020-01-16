def parse(filename):
    import csv
    from utilclasses import FullStatistics
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar = '|')
        groups = []
        block = []
        i = 0
        for row in reader:
            # print(','.join(row))
            if (i - 4) % 5 != 0:
                block.append(row)
            elif i != 0:
                groups.append(block.copy())
                block.clear()
            i += 1
        # questionlist = []
        if len(block) > 0:
            groups.append(block)
        # for group in groups:
        #     questionlist.append(Question(group))
        # comps = [Comparison("A", "B"), Comparison("A+B", "O")]
        # for question in questionlist:
        #     for comp in comps:
        #         print(question.compare(comp))
        comps = (("V1A", "V2A"), ("V1B", "V1A"), ("V2A", "V2B"), ("V1B", "V2B"), ("V1A+V2A", "V1B+V2B"), ("V1A+V1B", "V2A+V2B"), ("V1A+V1B+V2A+V2B", "O"), ("V1A+V1B", "O"), ("V2A+V2B", "O"), ("V1A+V2A", "O"), ("V1B+V2B", "O"))
        stats = FullStatistics(groups, comps)
        stats.evaluate("FinalExamAnalysis.txt")
