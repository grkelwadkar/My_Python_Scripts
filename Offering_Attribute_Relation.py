from lxml import etree
import cx_Oracle
import os

path = r'C:\Users\grkel\Downloads'
base_po_list = ['Fixed Voice PO R1', 'Data SIM PO R1', 'Internet PO R1', 'TV PO R1']

user = 'system'
pwd = 'system'
host = 'localhost'
port = '1521'
instance = 'XE'

dsn_tns = cx_Oracle.makedsn(host, port, instance)

conn = cx_Oracle.connect(user=user, password=pwd, dsn=dsn_tns)

cur = conn.cursor()

print('\n\nConnected to ' + user + '@' + instance)


rs = cur.execute("select count(*) from ALL_TABLES where table_name = 'OFFERING_ATTRIBUTE_RELATION'")

for row in rs:
    cnt = row[0]

if (cnt == 1):
    cur.execute('DROP TABLE OFFERING_ATTRIBUTE_RELATION')
    print('\n\nDropped table OFFERING_ATTRIBUTE_RELATION')

    cur.execute('''
   CREATE TABLE OFFERING_ATTRIBUTE_RELATION (
   PCVERSION_ID VARCHAR2(50),
   PO_NAME VARCHAR2(500),
   PO_ID VARCHAR2(100),
   PO_CODE VARCHAR2(100),
   ATTR_NAME_EN VARCHAR2(100),
   ATTR_NAME_IT VARCHAR2(100), 
   ATTR_ID VARCHAR2(100),
   ATTR_CODE VARCHAR2(100),
   DOMAIN_NAME VARCHAR2(100),
   DOMAIN_ID VARCHAR2(100),
   DEFAULTVALUE VARCHAR2(100))
   ''')

    print('\n\nCreated TABLE OFFERING_ATTRIBUTE_RELATION')
else:
    cur.execute('''
       CREATE TABLE OFFERING_ATTRIBUTE_RELATION (
       PCVERSION_ID VARCHAR2(50),
       PO_NAME VARCHAR2(500),
       PO_ID VARCHAR2(100),
       PO_CODE VARCHAR2(100),
       ATTR_NAME_EN VARCHAR2(100),
       ATTR_NAME_IT VARCHAR2(100), 
       ATTR_ID VARCHAR2(100),
       ATTR_CODE VARCHAR2(100),
       DOMAIN_NAME VARCHAR2(100),
       DOMAIN_ID VARCHAR2(100),
       DEFAULTVALUE VARCHAR2(100))''')

    print('\n\nCreated TABLE OFFERING_ATTRIBUTE_RELATION')



for offerfile in os.listdir(path):
    if offerfile.endswith('.xml') and offerfile.find('ProductOffering') != -1:
        print('\n\nWorking on file '+ offerfile)
        catalog_version = offerfile.replace('ProductOffering_','').replace('.xml','')
        #print(catalog_version)

        file = os.path.join(path, offerfile)

        root = etree.parse(file)

        for g in root.xpath('.//ProductOffering'):

            #print(100 * "-")
            po_name = g.find('.//Name//Value[@locale="en"]')
            po_name = po_name.text if po_name is not None else None

            if po_name in base_po_list:
                continue

            print('\n'+po_name)

            po_id = g.find('.//ProductOfferingVersions//ProductOfferingVersion//ID[@value]')
            po_id = po_id.get('value') if po_id is not None else None
            print('\n'+po_id)

            po_code = g.find('.//ProductOfferingVersions//ProductOfferingVersion//Code[@value]')
            po_code = po_code.get('value') if po_code is not None else None
            print('\n'+po_code)

            prodattrrels = g.findall('.//ProductAttributeRelation//ProductAttributeRelation')
            print(prodattrrels)

            for prodattrrel in prodattrrels:
                print(prodattrrel)

                #assignattr = prodattrrel.find('.//AssignableAttribute')

                #print(assignattr)

                attr_name_en = prodattrrel.find('.//AssignableAttribute//Name//Value[@locale="en"]')
                attr_name_it = prodattrrel.find('.//AssignableAttribute//Name//Value[@locale="it"]')
                attr_name_en = attr_name_en.text if attr_name_en is not None else None
                print('\n' + attr_name_en)

                attr_name_it = attr_name_it.text if attr_name_it is not None else None
                print('\n' + attr_name_it)

                attr_id = prodattrrel.find('.//AssignableAttribute//UniqueFields//Field[@name="ID"]')
                attr_id = attr_id.get('value') if attr_id is not None else None
                print('\n' + attr_id)

                attr_code = prodattrrel.find('.//AssignableAttribute//UniqueFields//Field[@name="Code"]')
                attr_code = attr_code.get('value') if attr_code is not None else None
                print('\n' + attr_code)

                domain_name = prodattrrel.find('.//Domain//Name//Value[@locale="it"]')
                domain_name = domain_name.text if domain_name is not None else None
                print('\n' + domain_name)

                domain_id = prodattrrel.find('.//Domain//UniqueFields//Field[@name="ID"]')
                domain_id = domain_id.get('value') if domain_id is not None else None
                print('\n' + domain_id)

                defaultvalue = prodattrrel.find('.//DefaultValue')
                defaultvalue = defaultvalue.get('value') if defaultvalue is not None else None
                print(defaultvalue)

                cur.execute(
                    "insert into OFFERING_PRICE_RELATION (PCVERSION_ID,PO_NAME,PO_ID,PO_CODE,ATTR_NAME_EN,ATTR_NAME_IT, ATTR_ID,ATTR_CODE,DOMAIN_NAME,DOMAIN_ID,DEFAULTVALUE) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)",
                    [catalog_version, po_name, po_id, po_code, attr_name_en,attr_name_it, attr_id,attr_code, domain_name, domain_id,defaultvalue])

conn.commit()
cur.close()
conn.close()