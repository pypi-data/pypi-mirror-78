from nose.case import Test
from nose.plugins.xunit import id_split


def get_test_names(test):
    names = []

    def dfs(case):
        if type(case) is Test:
            class_name, name = id_split(case.id())
            names.append({"className": class_name, "name": name})
            return

        for t in case._tests:
            dfs(t)

    dfs(test)
    return names


def reorder(test, order):
    table = {}
    for i, t in enumerate(order):
        table[(t["className"], t["name"])] = i

    def dfs(case):
        if type(case) is Test:
            cls, name = id_split(case.id())

            return table[(cls, name)], case

        cases = []
        total_index = 0
        # TODO: Improve the reducing algorithm
        for i, c in sorted([dfs(t) for t in case._tests], key=lambda x: x[0]):
            cases.append(c)
            total_index += i

        case._tests = cases

        # Avoid dividing with zero when 'cases' are empty
        return total_index / max(1, len(cases)), case

    return dfs(test)[1]


