import xmltodict

def xmlTodict(arg):
    return xmltodict.parse(arg,encoding='utf-8')