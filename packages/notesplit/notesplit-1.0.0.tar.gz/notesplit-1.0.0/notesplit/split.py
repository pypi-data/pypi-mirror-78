#!/usr/bin/python3
import json, re, os, argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='Source text file to parse.')
    parser.add_argument('-g', '--groups', help='Groups definitions json file.')
    args = parser.parse_args()

    SOURCE = args.source # e.g., 'OnePage.wiki'
    GROUPS = args.groups # e.g., 'GroupDefinitions.wiki'

    group_defs = json.load(open(GROUPS, 'r'))
    indiv, groups  = group_defs['individuals'], group_defs['groups']
    for k, g in groups.items(): groups[k] = frozenset(g)

    stack = []
    cur = stack
    for tok in re.compile('({:|\||:})').split(open(SOURCE, 'r').read()):
        if tok == '{:':   new = []; cur += [new]; stack += [cur]; cur = new
        elif tok == ':}': cur = stack.pop()
        else:             cur += [tok]

    out = { k:'' for k in indiv }
    def process(stack, group):
        if len(stack) >= 2 and stack[1] == '|':
            if stack[0][0] == '-':
                group = group - groups.get(stack[0][1:], set([stack[0][1:]]))
            else:
                group = group | groups.get(stack[0], set([stack[0]]))
            stack = stack[2:]
        for foo in stack:
            if type(foo) is list:
                process(foo, group)
            else:
                for who in group: out[who] += foo
    process(stack, frozenset())

    for who, data in out.items():
        if not os.path.exists("./%s" % (indiv[who],)):
            os.makedirs(indiv[who])
        open("{}/{}".format(indiv[who],SOURCE), 'w').write(data)


if __name__ == '__main__':
    main()
