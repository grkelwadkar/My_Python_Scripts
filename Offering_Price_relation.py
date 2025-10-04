from lxml import etree
import cx_Oracle
import os

path = r'C:\Users\grkel\Downloads'
base_po_list = ['Fixed Voice PO R1', 'Data SIM PO R1', 'Internet PO R1', 'TV PO R1']

user = 'system'
pwd = 'tiger'
host = 'localhost'
port = '1521'
instance = 'XE'

dsn_tns = cx_Oracle.makedsn(host, port, instance)

conn = cx_Oracle.connect(user=user, password=pwd, dsn=dsn_tns)

cur = conn.cursor()

print('\n\nConnected to ' + user + '@' + instance)


rs = cur.execute("select count(*) from ALL_TABLES where table_name = 'OFFERING_PRICE_RELATION'")

for row in rs:
    cnt = row[0]

if (cnt == 1):
    cur.execute('DROP TABLE OFFERING_PRICE_RELATION')
    print('\n\nDropped table OFFERING_PRICE_RELATION')
    cur.execute('''
   CREATE TABLE OFFERING_PRICE_RELATION
   (
   PCVERSION_ID VARCHAR2(50),
   PO_NAME VARCHAR2(500),
   PO_ID VARCHAR2(50),
   PO_CODE VARCHAR2(500),
   RELATION_ID VARCHAR2(50),
   PARENT_RELATION_ID VARCHAR2(50),
   REFINEMENT_ID VARCHAR2(50),
   BO_NAME VARCHAR2(500),
   BO_ID VARCHAR2(50),
   BO_CAPTION VARCHAR2(500),
   INCLUSION VARCHAR2(500),
   ENABLE_FOR_SELECTION VARCHAR2(50),
   REFINED_ID VARCHAR2(50),
   ISEXCLUDED VARCHAR2(500))
   ''')
    print('\n\nCreated TABLE OFFERING_PRICE_RELATION')
else:
    cur.execute('''
   CREATE TABLE OFFERING_PRICE_RELATION
   (
   PCVERSION_ID VARCHAR2(50),
   PO_NAME VARCHAR2(500),
   PO_ID VARCHAR2(50),
   PO_CODE VARCHAR2(500),
   RELATION_ID VARCHAR2(50),
   PARENT_RELATION_ID VARCHAR2(50),
   REFINEMENT_ID VARCHAR2(50),
   BO_NAME VARCHAR2(500),
   BO_ID VARCHAR2(50),
   BO_CAPTION VARCHAR2(500),
   INCLUSION VARCHAR2(500),
   ENABLE_FOR_SELECTION VARCHAR2(50),
   REFINED_ID VARCHAR2(50),
   ISEXCLUDED VARCHAR2(500))
   ''')
    print('\n\nCreated TABLE OFFERING_PRICE_RELATION')



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

            offerprodrels = g.findall('.//OfferingProductRelation//OfferingProductRelation')
            # print(offerprodrels)

            for offerprodrel in offerprodrels:
                refinedpricerelations = offerprodrel.findall('.//RefinedPriceRelation//RefinedPriceRelation')
                # print(refinedpricerelations)

                for refinedpricerelation in refinedpricerelations:
                    # print(refinedpricerelation)

                    relationID = refinedpricerelation.find('.//RelationID[@value]')
                    relationID = relationID.get('value') if relationID is not None else None
                    print('\n'+relationID)

                    parentRelationID = refinedpricerelation.find('.//ParentRelationID[@value]')
                    parentRelationID = parentRelationID.get('value') if parentRelationID is not None else None
                    print('\n'+parentRelationID)

                    ID = refinedpricerelation.find('.//ID[@value]')
                    ID = ID.get('value') if ID is not None else None
                    print('\n'+ID)

                    priceName = refinedpricerelation.find('.//Price//Name//Value[@locale="en"]')
                    priceName = priceName.text if priceName is not None else None
                    print('\n'+priceName)

                    bo_id = refinedpricerelation.find('.//Price//UniqueFields//Field[@name="ID"]')
                    bo_id = bo_id.get('value') if bo_id is not None else None
                    print('\n'+bo_id)

                    bo_code = refinedpricerelation.find('.//Price//UniqueFields//Field[@name="Code"]')
                    bo_code = bo_code.get('value') if bo_code is not None else None
                    print('\n'+bo_code)

                    inclusion = refinedpricerelation.find('.//Inclusion//Name//Value[@locale="en"]')
                    inclusion = inclusion.text if inclusion is not None else None
                    print('\n'+inclusion)

                    enableForSelection = refinedpricerelation.find('.//EnableForSelection[@value]')
                    enableForSelection = enableForSelection.get('value') if enableForSelection is not None else None
                    print('\n'+enableForSelection)

                    refinedID = refinedpricerelation.find('.//RefinedID[@value]')
                    refinedID = refinedID.get('value') if refinedID is not None else None
                    print(refinedID)

                    IsExcluded = refinedpricerelation.find('.//IsExcluded[@value]')
                    IsExcluded = IsExcluded.get('value') if IsExcluded is not None else None

                    print(IsExcluded)

                    #print(100 * "-")

                    cur.execute(
                        "insert into OFFERING_PRICE_RELATION (PCVERSION_ID,PO_NAME,PO_ID,PO_CODE ,RELATION_ID,PARENT_RELATION_ID, REFINEMENT_ID,BO_NAME,BO_ID,BO_CAPTION,INCLUSION,ENABLE_FOR_SELECTION, REFINED_ID,ISEXCLUDED ) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14)",
                        [catalog_version,po_name, po_id, po_code, relationID, parentRelationID, ID, priceName, bo_id, bo_code,
                         inclusion, enableForSelection, refinedID, IsExcluded])

conn.commit()
cur.close()
conn.close()