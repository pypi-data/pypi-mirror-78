def striplist(list):
    out = []
    for i in list:
        stin = str(i)
        split = (stin.split('>'))
        otherside = (split[1].split('<'))
        out_app = otherside[0]
        out.append(out_app)

    return out


def find_between(s, first, last):
    try:
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            start = s.index(first) + len(first)
            return s[start:]

    except BaseException as e:
        print(e, first, last)
        return 'NA'
