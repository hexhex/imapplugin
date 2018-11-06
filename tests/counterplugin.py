import acthex
from imapplugin import ImapEnvironment


def count_evaluation():
    print("called count_evaluation")
    acthex.environment().counter += 1

def get_evaluations():
    print("called get_evaluations", acthex.environment().counter)
    acthex.output((acthex.environment().counter,))

def register():
    acthex.addAction('count_evaluation', ())
    acthex.addAtom('get_evaluations', (), 1)
    acthex.setEnvironment(ImapTestEnvironment())


class ImapTestEnvironment(ImapEnvironment):
    counter = 0

    def __init__(self):
        print("called ImapTestEnvironment constructor")