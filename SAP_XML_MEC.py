from lxml import etree
import cx_Oracle
import os

curdir = r'C:\Users\grkel\Downloads\SAP_XML'

usr = 'hr'
pwd = 'hr'
host = 'localhost'
port = '1521'
instance = 'XEPDB1'

conn = cx_Oracle.connect(user="hr", password="hr",
                         dsn="localhost:1521/XEPDB1",
                         encoding="UTF-8")

cur = conn.cursor()

print('\n\nConnected to ' + usr + '@' + instance)

rs = cur.execute("select count(*) from all_objects where object_name = 'SAP_DEVICE_DATA' and object_type = 'TABLE'")

for row in rs:
    cnt = row[0]

if cnt == 1:
    cur.execute("DROP TABLE SAP_DEVICE_DATA")
    print("\n\nDropped table SAP_DEVICE_DATA..")
    cur.execute('''CREATE TABLE SAP_DEVICE_DATA
            (SAP_ID VARCHAR2(20 BYTE),
          MATERIAL_DESCRIPTION VARCHAR2(500 BYTE),
          MATERIAL_GROUP VARCHAR2(30 BYTE),
            MATERIAL_KIT VARCHAR2(30 BYTE),
            BRAND VARCHAR2(30 BYTE),
            COLOR VARCHAR2(30 BYTE),
            MODEL VARCHAR2(30 BYTE),
            SALES_ARTICLE VARCHAR2(30 BYTE),
            SALES_DETAILS VARCHAR2(30 BYTE),
            SSP_RATE VARCHAR2(30 BYTE),
            SSP_CURRENCY VARCHAR2(30 BYTE),
            SAP_FILE_NAME VARCHAR2(100 BYTE)
            )''')

    print("\n\nCreated table SAP_DEVICE_DATA..")
else:
    cur.execute('''CREATE TABLE SAP_DEVICE_DATA 
                (SAP_ID VARCHAR2(20 BYTE),
              MATERIAL_DESCRIPTION VARCHAR2(500 BYTE),
              MATERIAL_GROUP VARCHAR2(30 BYTE),
                MATERIAL_KIT VARCHAR2(30 BYTE),
                BRAND VARCHAR2(30 BYTE),
                COLOR VARCHAR2(30 BYTE),
                MODEL VARCHAR2(30 BYTE),
                SALES_ARTICLE VARCHAR2(30 BYTE),
                SALES_DETAILS VARCHAR2(30 BYTE),
                SSP_RATE VARCHAR2(30 BYTE),
                SSP_CURRENCY VARCHAR2(30 BYTE)
                SAP_FILE_NAME VARCHAR2(100 BYTE))
                ''')
    print("\n\nCreated table SAP_DEVICE_DATA..")


rs = cur.execute("select count(*) from all_objects where object_name = 'SAP_DEVICE_DATA_REFINED' and object_type = 'TABLE'")

for row in rs:
    cnt = row[0]

if cnt == 1:
    cur.execute("DROP TABLE SAP_DEVICE_DATA_REFINED")
    print("\n\nDropped table SAP_DEVICE_DATA_REFINED..")
    cur.execute('''CREATE TABLE SAP_DEVICE_DATA_REFINED
            (SAP_ID VARCHAR2(20 BYTE),
          MATERIAL_DESCRIPTION VARCHAR2(500 BYTE),
          MATERIAL_GROUP VARCHAR2(30 BYTE),
            MATERIAL_KIT VARCHAR2(30 BYTE),
            BRAND VARCHAR2(30 BYTE),
            COLOR VARCHAR2(30 BYTE),
            MODEL VARCHAR2(30 BYTE),
            SALES_ARTICLE VARCHAR2(30 BYTE),
            SALES_DETAILS VARCHAR2(30 BYTE),
            SSP_RATE VARCHAR2(30 BYTE),
            SSP_CURRENCY VARCHAR2(30 BYTE))
            ''')

    print("\n\nCreated table SAP_DEVICE_DATA_REFINED..")
else:
    cur.execute('''CREATE TABLE SAP_DEVICE_DATA_REFINED 
                (SAP_ID VARCHAR2(20 BYTE),
              MATERIAL_DESCRIPTION VARCHAR2(500 BYTE),
              MATERIAL_GROUP VARCHAR2(30 BYTE),
                MATERIAL_KIT VARCHAR2(30 BYTE),
                BRAND VARCHAR2(30 BYTE),
                COLOR VARCHAR2(30 BYTE),
                MODEL VARCHAR2(30 BYTE),
                SALES_ARTICLE VARCHAR2(30 BYTE),
                SALES_DETAILS VARCHAR2(30 BYTE),
                SSP_RATE VARCHAR2(30 BYTE),
                SSP_CURRENCY VARCHAR2(30 BYTE))
                ''')
    print("\n\nCreated table SAP_DEVICE_DATA_REFINED..")

for file in os.listdir(curdir):
    print("Working on file ..."+file)



    filename = os.path.join(curdir, file)
    root = etree.parse(filename)

    for g in root.xpath('.//SAPEquipment'):
        SAP_ID_SAP = g.find('.//SAP_MATERIAL_ID')

        SAP_ID_SAP = SAP_ID_SAP.text if SAP_ID_SAP is not None else None

        print(SAP_ID_SAP + '------->')

        Material_Description = g.find('.//Material_Description')

        Material_Description = Material_Description.text if Material_Description is not None else None

        print(Material_Description)

        Material_Group = g.find('.//Material_Group')

        Material_Group = Material_Group.text if Material_Group is not None else None

        print(Material_Group)

        Material_KIT = g.find('.//Material_KIT')

        Material_KIT = Material_KIT.text if Material_KIT is not None else None

        print(Material_KIT)

        attribs = g.findall('.//Attrib_list//Attribute')

        brand = attribs[0].find('.//value').text

        color = attribs[1].find('.//value').text

        model = attribs[2].find('.//value').text

        sales_article = attribs[3].find('.//value').text

        sales_details = attribs[4].find('.//value').text

        print(brand)

        print(color)

        print(model)

        print(sales_article)

        print(sales_details)

        SSP = g.find('.//SSP')

        SSP = SSP.text if SSP is not None else None

        print(SSP)

        SSP_CURRENCY = g.find('.//SSP_CURRENCY')

        SSP_CURRENCY = SSP_CURRENCY.text if SSP_CURRENCY is not None else None

        print(SSP_CURRENCY)

        cur.execute(
            "insert into SAP_DEVICE_DATA (SAP_ID , MATERIAL_DESCRIPTION , MATERIAL_GROUP , MATERIAL_KIT , BRAND, COLOR, MODEL, SALES_ARTICLE, SALES_DETAILS,SSP_RATE,SSP_CURRENCY,SAP_FILE_NAME) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12)",
            [SAP_ID_SAP, Material_Description, Material_Group, Material_KIT, brand, color, model, sales_article,
             sales_details, SSP, SSP_CURRENCY, file])



        conn.commit()


cur.execute("insert into SAP_DEVICE_DATA_REFINED select distinct SAP_ID , MATERIAL_DESCRIPTION , MATERIAL_GROUP , MATERIAL_KIT , BRAND, COLOR, MODEL, SALES_ARTICLE, SALES_DETAILS,SSP_RATE,SSP_CURRENCY from SAP_DEVICE_DATA")

conn.commit()

cur.close()
conn.close()