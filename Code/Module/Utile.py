"""
Define function.
"""


def makefolder(dirname):
    """
    :param dirname: This param is path which you want to make folder.
    :return: Print.
    """
    import os

    if type(dirname) == list:
        for dn in dirname:
            if not os.path.isdir(dn):
                os.makedirs(dn)

                return print("Make folder : {}".format(dn))
    else:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

            return print("Make folder : {}".format(dirname))


def makedate(startdate, enddate):
    """
    :param startdate: Start date (format is 'YYYYMMDDHH')
    :param enddate: End date
    :return:
    """
    import datetime as d

    FromDateTime = d.datetime.strptime(str(int(startdate)), "%Y%m%d%H")
    ToDateTime = d.datetime.strptime(str(int(enddate)), "%Y%m%d%H")
    DateList = []
    NowDateTime = FromDateTime
    while NowDateTime <= ToDateTime:
        YYYY = str(NowDateTime.year).zfill(4)
        MM = str(NowDateTime.month).zfill(2)
        DD = str(NowDateTime.day).zfill(2)
        HH = str(NowDateTime.hour).zfill(2)
        Format = int(str("{}{}{}{}".format(YYYY, MM, DD, HH))) + 1
        DateList.append(Format)
        NowDateTime = NowDateTime + d.timedelta(hours=1)

    return DateList


def deletefolder(dirname):
    """
    :param dirname: This param is path which you want to delete folder.
    :return: Print.
    """
    import shutil

    if type(dirname) == list:
        for dn in dirname:
            shutil.rmtree(dn)

            return print("delete folder : {}".format(dn))

    else:
        shutil.rmtree(dirname)

        return print("delete folder : {}".format(dirname))
