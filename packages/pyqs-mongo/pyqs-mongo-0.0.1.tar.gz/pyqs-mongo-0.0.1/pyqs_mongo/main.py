from pyqs_mongo import parse
if __name__ == '__main__':
    print(parse('name=ahmed&company=someCompany&age=>=20&age=<=50&username=[]ahmed&username=[]adh&username=[!]some'))
