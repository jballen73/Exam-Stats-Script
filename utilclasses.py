class Stats:
    def __init__(self, name, mean, std, n):
        self.name = name
        self.mean = float(mean)
        self.std = float(std)
        self.n = int(n)

    def __str__(self):
        return "Name: {0}\nMean: {1}\nStD: {2}\nN: {3}".format(self.name, self.mean, self.std, self.n)

    def __add__(self, other):
        if other == 0:
            return self
        sx1 = self.mean * self.n
        sx2 = other.mean * other.n

        v1 = (self.std**2)*(self.n - 1) + ((sx1**2)/self.n)
        v2 = (other.std ** 2) * (other.n - 1) + ((sx2 ** 2) / other.n)

        tn = self.n + other.n
        tx = sx1 + sx2
        txx = v1 + v2

        newname = self.name + " + " + other.name
        from math import sqrt
        return Stats(newname, tx/tn, sqrt((txx - (tx**2)/tn)/(tn - 1)), tn)

    def __radd__(self, other):
        return self + other


class Comparison:
    def __init__(self, comp):
        left = comp[0].split("+")
        right = comp[1].split("+")
        self.comp = (left, right)

    def __getitem__(self, item):
        return self.comp[item]

    def __str__(self):
        return "{0} vs. {1}".format("+".join(self[0]), "+".join(self[1]))


class Question:
    def __init__(self, data, from_gui=False):
        if from_gui:
            self.name = data['name']
            self.stats = data['stats']
            self.groups = data['groups']
        else:
            self.name = data[0][0]
            self.stats = {}
            self.groups = []
            for j in range(1, len(data[0])):
                    if data[0][j] != "":
                        self.groups.append(data[0][j])
                        self.stats[data[0][j]] = (Stats(data[0][j], data[1][j], data[2][j], data[3][j]))

    def __str__(self):
        result = "Name: " + str(self.name) + "\n"
        for i, group in enumerate(self.groups):
            result += "Group {0}:\n".format(i+1)
            result += str(self.stats[group]) + "\n"
        return result

    def compare(self, comparison):
        left, right = comparison
        for group in left:
            if group not in self.groups:
                return "{0}: N/A".format(str(comparison))
        for group in right:
            if group not in self.groups:
                return "{0}: N/A".format(str(comparison))

        if len(left) == 1 and len(right) == 1:
            p, g1m, g1s, g2m, g2s = self.compare_groups(left[0], right[0])
            return "{}: p = {}, ({:.2f}, {:.2f} vs {:.2f}, {:.2f})".format(str(comparison), p, g1m, g1s, g2m, g2s)
        else:
            left = sum(list(map(lambda x: self.stats[x], left)))
            right = sum(list(map(lambda x: self.stats[x], right)))
            p, g1m, g1s, g2m, g2s = self.compare_groups(left, right)
            return "{}: p = {}, ({:.2f}, {:.2f} vs {:.2f}, {:.2f})".format(str(comparison), p, g1m, g1s, g2m, g2s)

    def compare_groups(self, group1, group2, equal_var=True):
        if isinstance(group1, Stats) and isinstance(group2, Stats):
            stat = group1
            g1m = stat.mean
            g1s = stat.std
            g1n = stat.n
            stat = group2
            g2m = stat.mean
            g2s = stat.std
            g2n = stat.n
        if group1 in self.stats:
            stat = self.stats[group1]
            g1m = stat.mean
            g1s = stat.std
            g1n = stat.n
        if group2 in self.stats:
            stat = self.stats[group2]
            g2m = stat.mean
            g2s = stat.std
            g2n = stat.n
        from scipy.stats import ttest_ind_from_stats
        t, p = ttest_ind_from_stats(g1m, g1s, g1n, g2m, g2s, g2n, equal_var=equal_var)
        return p, g1m, g1s, g2m, g2s

class FullStatistics:
    def __init__(self, data, comparisons, from_gui=False):
        self.questions = []
        if from_gui:
            self.questions = data
        else:
            for group in data:
                self.questions.append(Question(group))
        self.comparisons = []
        for comp in comparisons:
            self.comparisons.append(Comparison(comp))


    def evaluate(self, filename):
        # import csv
        with open(filename, 'w', newline='') as file:
            # csvwriter = csv.writer(csvfile, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONNUMERIC)
            for question in self.questions:
                print("Question: " + question.name, file=file)
                for comp in self.comparisons:
                    print(question.compare(comp), file=file)