from utilclasses import *
def convert_gui_output_to_fullstatistics(versions, questions, comps, filename):
    question_list = []
    for question in questions:
        q_dict = {}
        q_dict['name'] = str(question)
        q_dict['stats'] = {}
        q_dict['groups'] = []
        for (name_number, stats) in versions.items():
            if question in stats:
                new_stat = Stats(name_number[0], stats[question][0], stats[question][1], name_number[1])
                q_dict['stats'][name_number[0]] = new_stat
                q_dict['groups'].append(name_number[0])
        new_question = Question(q_dict, from_gui=True)
        question_list.append(new_question)
    # comps = (("VA", "VB"), ("VA", "VO"))
    fullstats = FullStatistics(question_list, comps, from_gui=True)
    fullstats.evaluate(filename)