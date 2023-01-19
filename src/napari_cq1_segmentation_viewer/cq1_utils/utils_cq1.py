def getWellName(cq1ID: str) -> str:
    '''
    Gets the conventional well name for a given CQ1 image name.
    :param cq1ID: (str) filename
    :return: (str) conventional well name (empty string if wrong CQ1-ID)
    '''
    cq1IDstart = cq1ID[0:5]
    dic = dictIDtoWell()
    if not cq1IDstart.startswith('W'):
        raise Exception(f"Well name is wrong: {cq1ID}")
    if not (cq1IDstart in dic.keys()):
        return ''
    return dic[cq1IDstart]


def dictIDtoWell() -> dict:
    '''
    Create a dictionary with keys = CQ1 well IDs
    and values with the conventional well names (e.g. A01)
    :return: dictionary
    '''
    row_count = 0
    rowNames = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
    dic = {}

    for well in range(1,385):
        cq1ID = "W%04d" % (well)
        if well % 24 == 0:
            dic[cq1ID] = rowNames[row_count] + "24"
            #print(rowNames[row_count] + "24")
            row_count += 1
        else:
            dic[cq1ID] = rowNames[row_count] + "%02d" % (well%24)
            #print(rowNames[row_count] + "%02d" % (well % 24))
    return dic
