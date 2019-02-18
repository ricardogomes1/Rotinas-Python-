"""edit_distance.py: find the edit distance between two strings.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)

This is problem 526:

    http://acm.uva.es/p/v5/526.html

of the ACM International Collegiate Programming Contest:

    http://acm.uva.es/problemset/

We find the minimum number of manipulations we need to do to get from
one string to another.  We can do any of the following:

    Insert a character
    Delete a character
    Replace a character

each of which we'll assume will "cost" 1.


For example, to get from:

    "abcac" to "bcd"

requires the following manipulations:

    1.  Delete the first character.
    2.  Replace the third character with a d.
    3.  Delete the fourth character.

so the string starts evolving like this:

    "abcac" --> "bcac" --> "bcdc" --> "bcd"

and we'd say that this edit distance is 3.  There are several possible
ways to get from one string to another; we're just looking for one
possible solution.

The interesting functions in here are: getEditDistance() and
getDescriptiveEditDistance().
"""

import operator
import sys
import StringIO


def getEditDistance(begin, end):
    """Given strings "begin" and "end", returns the edit distance
    between them."""
    begin, end = [None] + list(begin), [None] + list(end)
    n, m = len(begin), len(end)
    table = initializeEditTable(m, n)
    for i in range(1, n):
        for j in range(1, m):
            replace_cost = table[i-1][j-1] + 1
            if begin[i] == end[j]: replace_cost -= 1
            table[i][j] = min(table[i-1][j] + 1,
                              table[i][j-1] + 1,
                              replace_cost)
    return table[-1][-1]


def initializeEditTable(m, n):
    """Helper function: set up the edit table's borders."""
    table = makeNxM(n, m)
    for i in range(n): table[i][0] = i
    for i in range(m): table[0][i] = i
    return table



######################################################################

def getDescriptiveEditDistance(begin, end):
    """Given strings "begin" and "end", returns the sequence of
    manipulations needed to change "begin" to the "end"."""
    table = getDescriptiveEditTable(begin, end)
    trail = getDescriptiveEditTrail(table, begin, end)
    description = []
    counter = 1
    for i in range(len(trail) - 1):
        delta = tupleSubtract(trail[i+1], trail[i])
        j, k = trail[i+1]
        if delta == (0, 1):    ## Insert
            description.append("Insert %s,%s" % (counter, end[k-1]))
            counter += 1
        elif delta == (1, 0):  ## Delete
            description.append("Delete %s" % counter)
        else:                  ## Replace
            if table[j][k][0] == table[j-1][k-1][0]:
                pass
            else:
                description.append("Replace %s,%s" % (counter, end[k-1])) 
            counter += 1
    return description


def getDescriptiveEditTrail(table, begin, end):
    """Helper functoin: return the path we take through the edit table
    to get to our end word."""
    edit_trail = []
    i, j = len(begin), len(end)
    while (i, j) != (0, 0):
        sentinel, next_jump = table[i][j]
        edit_trail.append((i, j))
        i, j = next_jump
    edit_trail.append((0, 0))
    edit_trail.reverse()
    return edit_trail


def getDescriptiveEditTable(begin, end):
    """Helper function: given words begin and end, return the edit
    table whose entries consist of the tuple:
        (acccumlated_cost, (parent_i, parent_j))."""
    begin, end = [None] + list(begin), [None] + list(end)
    n, m = len(begin), len(end)
    table = initializeDescriptiveEditTable(m, n)
    for i in range(1, n):
        for j in range(1, m):
            table[i][j] = chooseDescriptiveMinimum(i, j, table, begin, end)
    return table


def chooseDescriptiveMinimum(i, j, table, begin, end):
    """Helper function: choose the best manipulation out of insertion,
    deletion, and replacement."""
    (insert_cost, delete_cost) = (table[i][j-1][0] + 1,
                                  table[i-1][j][0] + 1)
    replace_cost = table[i-1][j-1][0] + 1
    if begin[i] == end[j]: replace_cost -= 1

    if replace_cost <= insert_cost and replace_cost <= delete_cost:
        return (replace_cost, (i-1, j-1))
    if insert_cost <= replace_cost and insert_cost <= delete_cost:
        return (insert_cost, (i, j-1))
    else:
        return (delete_cost, (i-1, j))


def initializeDescriptiveEditTable(m, n):
    """Helper function: initialize the corners of the edit table."""
    table = makeNxM(n, m)
    for i in range(n): table[i][0] = (i, (i-1, 0))
    for i in range(m): table[0][i] = (i, (0, i-1))
    return table


def makeNxM(n, m):
    """Returns an n x m table initially filled with None's."""
    table = [None] * n
    for i in range(n):
        table[i] = [None] * m
    return table


def tupleSubtract(t1, t2):
    """Given tuples t1 and t2, returns the componentwise difference
    between them.

    For example:

        tupleSubtract((1, 2, 3), (3, 2, 1)) ==> (-2, 0, 2)."""
    pairs = zip(t1, t2)
    diffs = map(lambda t: apply(operator.sub, t), pairs)
    return tuple(diffs)




######################################################################
## Scaffold code for testing and using this as a utility

def _driver(file):
    while 1:
        l1, l2 = file.readline(), file.readline()
        if l1 == "" or l2 == "": break
        l1, l2 = l1.rstrip(), l2.rstrip()
        edits = getDescriptiveEditDistance(l1, l2)
        print len(edits)
        for i in range(len(edits)):
            print i+1, edits[i]


def _test():
    """A small test to see if things are working."""
    stringfile = StringIO.StringIO("""abcac
bcd
aaa
aabaaaa""")
    _driver(stringfile)


if __name__ == '__main__':
    _driver(sys.stdin)
