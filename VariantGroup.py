#!/usr/bin/env python

# encoding: utf-8

from lxml import etree
from datetime import datetime
import cx_Oracle
import ConfigParser
import zipfile
import os
import getpass
import sys
import random

config = ConfigParser.RawConfigParser()
config.read('env.properties')


class bcolors:
    GREEN = '\033[92m'  # GREEN
    YELLOW = '\033[93m'  # YELLOW
    RED = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


lst = ["A bad workman always blames his tools.",
       "A bird in hand is worth two in the bush.",
       "Absence makes the heart grow fonder.",
       "A cat has nine lives.",
       "A chain is only as strong as its weakest link.",
       "Actions speak louder than words.",
       "A drowning man will clutch at a straw.",
       "Adversity and loss make a man wise.",
       "A fool and his money are soon parted.",
       "A journey of thousand miles begins with a single step.",
       "'The greatest glory in living lies not in never falling, but in rising every time we fall.' -Nelson Mandela",
       "All good things come to an end.",
       "All's well that ends well.",
       "'Life is what happens when you're busy making other plans.' -John Lennon",
       "'When you reach the end of your rope, tie a knot in it and hang on.' -Franklin D. Roosevelt",
       "If you prick us do we not bleed? If you tickle us do we not laugh? If you poison us do we not die? And if you wrong us shall we not revenge?",
       "All's fair in love and war.",
       "All that glitters is not gold.",
       "A cada cerdo le llega su San Martin.",
       "'Life is a long lesson in humility.' -James M. Barrie",
       "'Don\'t judge each day by the harvest you reap but by the seeds that you plant.' -Robert Louis Stevenson",
       "El que la hace, la paga.",
       "'I find that the harder I work, the more luck I seem to have.' -Thomas Jefferson",
       "A mal tiempo, buena cara.",
       "Mas ven cuatro ojos que dos.",
       "Dime con quien andas, y te dire quien eres.",
       "Dios los cria, y ellos se juntan.",
       "'The purpose of our lives is to be happy.' -Dalai Lama",
       "Donde hay confianza, da asco.",
       "Hoy por ti, manana por mi.",
       "Desgraciado en el juego, afortunado en amores.",
       "El amor es ciego.",
       "Obras son amores, que no buenas razones.",
       "Mucho ruido y pocas nueces.",
       "A caballo regalado, no le mires el diente.",
       "Hope is the thing with feathers - That perches in the soul - And sings the tune without the words - And never stops at all",
       "At any given moment in the middle of a city there's a million epiphanies occurring, in the blurring of the world beyond the curtain",
       "Dying is nothing but it is terrible not to live"]
length = len(lst)

randomnum = random.randint(0, length - 1)

now = datetime.now()

print("\n\n")
print(bcolors.YELLOW + lst[randomnum] + bcolors.RESET)
print("\n\n")
print(bcolors.GREEN + 'Starting VariantGroup Import job at - ' + bcolors.YELLOW + str(now))
print("\n\n" + bcolors.GREEN)
# users = getpass.getuser()

username = str(raw_input("Please enter your name : "))

print("\n\n")

print(bcolors.GREEN + 'Initiated by User - ' + str(username))

# fdlocation = '/users/gen/abpwrk1/VariantGroup/FD'
fdlocation = config.get('ParseXML', 'fd.location')

print(bcolors.RED + '\n\nMake sure you have uploaded latest Distribution zip file under FD folder located at - ' + str(
    fdlocation) + bcolors.GREEN)

# print('Enter yes to continue or no to exit.......')
print("\n\n")

while True:
    input_user = str(raw_input('Enter yes to continue or no to exit....'))

    if input_user.lower() == 'no':
        print('Exiting...' + bcolors.RESET)
        sys.exit()
    elif input_user.lower() == 'yes':
        print('Thanks...Continuing...')
        break
    else:
        print('Please enter a valid input!!')

onlyfiles = [f for f in os.listdir(fdlocation) if os.path.isfile(os.path.join(fdlocation, f))]

# print(onlyfiles)

for f in onlyfiles:
    if f.find('.zip') != -1 and f.find('Distribution') != -1:
        zipfilename = f

print('\n\nDistribution zip file is - ' + zipfilename)

with zipfile.ZipFile('/users/gen/abpwrk1/VariantGroup/FD/' + zipfilename, 'r') as zip_ref:
    zip_ref.extractall('FD')

print('\n\nRunning Variant Group Table Importer from Variant Group XML....')

file = config.get('ParseXML', 'xml.file')

root = etree.parse(file)

print('\n\nTrying to connect to DB ....')

user = config.get('DatabaseSection', 'database.user')
pwd = config.get('DatabaseSection', 'database.password')
host = config.get('DatabaseSection', 'database.db_host')
port = config.get('DatabaseSection', 'database.db_port')
instance = config.get('DatabaseSection', 'database.db_instance')

dsn_tns = cx_Oracle.makedsn(host, port, instance)
conn = cx_Oracle.connect(user=user, password=pwd, dsn=dsn_tns)

cur = conn.cursor()

print('\n\nConnected to ' + user + '@' + instance)

rs = cur.execute("select count(*) from all_objects where object_name = 'VARIANTGROUPS' and object_type = 'TABLE'")

for row in rs:
    cnt = row[0]

if (cnt == 1):
    cur.execute("DROP TABLE VARIANTGROUPS")
    print("\n\nDropped table VARIANTGROUPS..")
    cur.execute('''CREATE TABLE VARIANTGROUPS
                   (
                       VG_ID             VARCHAR2(50 BYTE),
                       VG_NAME_EN        VARCHAR2(100 BYTE),
                       VG_NAME_IT        VARCHAR2(100 BYTE),
                       VG_CODE           VARCHAR2(50 BYTE),
                       VG_DESC           VARCHAR2(1000 BYTE),
                       VG_SALES_EFF_DT   DATE,
                       VG_SALES_EXP_DT   DATE,
                       VG_RANK           VARCHAR2(50 BYTE),
                       VG_SPS_VARIANT    VARCHAR2(1000 BYTE),
                       VG_SPS_IS_DEFAULT VARCHAR2(25 BYTE),
                       VARIANT_CID       VARCHAR2(50),
                       DEVICE_ID         VARCHAR2(50),
                       SKU               VARCHAR2(100),
                       DISTRIB_FILE_NAME VARCHAR2(100),
                       RUN_BY            VARCHAR2(50),
                       JOB_RUN_TIME      DATE
                   )''')
    print("\n\nCreated table VARIANTGROUPS..")
else:
    cur.execute('''CREATE TABLE VARIANTGROUPS
                   (
                       VG_ID             VARCHAR2(50 BYTE),
                       VG_NAME_EN        VARCHAR2(100 BYTE),
                       VG_NAME_IT        VARCHAR2(100 BYTE),
                       VG_CODE           VARCHAR2(50 BYTE),
                       VG_DESC           VARCHAR2(1000 BYTE),
                       VG_SALES_EFF_DT   DATE,
                       VG_SALES_EXP_DT   DATE,
                       VG_RANK           VARCHAR2(50 BYTE),
                       VG_SPS_VARIANT    VARCHAR2(1000 BYTE),
                       VG_SPS_IS_DEFAULT VARCHAR2(25 BYTE),
                       VARIANT_CID       VARCHAR2(50),
                       DEVICE_ID         VARCHAR2(50),
                       SKU               VARCHAR2(100),
                       DISTRIB_FILE_NAME VARCHAR2(100),
                       RUN_BY            VARCHAR2(50),
                       JOB_RUN_TIME      DATE
                   )''')

    print("\n\nCreated table VARIANTGROUPS..")

rs = cur.execute("select count(*) from all_objects where object_name = 'VARIANTGROUP_ATTRS' and object_type = 'TABLE'")

for row in rs:
    cnt = row[0]

if (cnt == 1):
    cur.execute("DROP TABLE VARIANTGROUP_ATTRS")
    print("\n\nDropped table VARIANTGROUP_ATTRS..")
    cur.execute('''CREATE TABLE VARIANTGROUP_ATTRS
                   (
                       VG_ID             VARCHAR2(50 BYTE),
                       VG_NAME_EN        VARCHAR2(100 BYTE),
                       VG_NAME_IT        VARCHAR2(100 BYTE),
                       VG_CODE           VARCHAR2(50 BYTE),
                       VG_DESC           VARCHAR2(1000 BYTE),
                       VG_SALES_EFF_DT   DATE,
                       VG_SALES_EXP_DT   DATE,
                       VG_RANK           VARCHAR2(50 BYTE),
                       VG_ATTRIB_NAME    VARCHAR2(1000 BYTE),
                       VG_ATTRIB_CODE    VARCHAR2(25 BYTE),
                       VG_ATTRIB_ID      VARCHAR2(50),
                       DEFAULT_VALUE     VARCHAR2(1000),
                       CONSTANT          VARCHAR2(50),
                       USE_AS_HIGHLIGHT  VARCHAR2(50),
                       USE_AS_VARIANT    VARCHAR2(50),
                       DISTRIB_FILE_NAME VARCHAR2(100),
                       RUN_BY            VARCHAR2(50),
                       JOB_RUN_TIME      DATE
                   )''')

    print("\n\nCreated table VARIANTGROUPS_ATTRS..")
else:
    cur.execute('''CREATE TABLE VARIANTGROUP_ATTRS
                   (
                       VG_ID             VARCHAR2(50 BYTE),
                       VG_NAME_EN        VARCHAR2(100 BYTE),
                       VG_NAME_IT        VARCHAR2(100 BYTE),
                       VG_CODE           VARCHAR2(50 BYTE),
                       VG_DESC           VARCHAR2(1000 BYTE),
                       VG_SALES_EFF_DT   DATE,
                       VG_SALES_EXP_DT   DATE,
                       VG_RANK           VARCHAR2(50 BYTE),
                       VG_ATTRIB_NAME    VARCHAR2(1000 BYTE),
                       VG_ATTRIB_CODE    VARCHAR2(25 BYTE),
                       VG_ATTRIB_ID      VARCHAR2(50),
                       DEFAULT_VALUE     VARCHAR2(1000),
                       CONSTANT          VARCHAR2(50),
                       USE_AS_HIGHLIGHT  VARCHAR2(50),
                       USE_AS_VARIANT    VARCHAR2(50),
                       DISTRIB_FILE_NAME VARCHAR2(100),
                       RUN_BY            VARCHAR2(50),
                       JOB_RUN_TIME      DATE
                   )''')
    print("\n\nCreated table VARIANTGROUP_ATTRS..")

print("\n\nParsing XML " + file + " and inserting data in table VARIANTGROUPS..")
for g in root.xpath('.//VariantGroup'):
    name_EN = g.find('.//Name/Value[@locale="en"]')
    name_IT = g.find('.//Name/Value[@locale="it"]')
    VG_ID = g.find('.//VariantGroupVersion/ID[@value]')
    VG_Code = g.find('.//VariantGroupVersion//Code[@value]')
    desc = g.find('.//Description/Value[@locale="it"]')
    sed = g.find('.//VariantGroupVersion/SaleEffectiveDate[@value]')
    sexd = g.find('.//VariantGroupVersion/SaleExpirationDate[@value]')
    r = g.find('.//RecommendationRank//RecommendationRank[@value]')
    variantRelations = g.findall('.//SPSVariantRelation//VariantGroupRelation')
    # print(variantRelations)

    # variants_ofid = g.findall('.//SPS//UniqueFields//Field[@name="ProductOfferingID"]')
    # variants_prid = g.findall('.//SPS//UniqueFields//Field[@name="ProductSpecID"]')
    # print('Included SPS (Variants) -', [v.text for v in variants])
    for v in variantRelations:
        dev_name_en = name_EN.text if name_EN is not None else None
        dev_name_it = name_IT.text if name_IT is not None else None
        dev_id = VG_ID.get('value') if VG_ID is not None else None
        dev_code = VG_Code.get('value') if VG_Code is not None else None
        dev_desc = desc.get('value') if desc is not None else None

        dev_eff = sed.get('value') if sed is not None else None

        if dev_eff is not None:
            dev_eff = datetime.strptime(dev_eff, "%Y-%m-%dT%H:%M:%S")
        else:
            dev_eff = None
        dev_exp = sexd.get('value') if sexd is not None else None
        if dev_exp is not None:
            dev_exp = datetime.strptime(dev_exp, "%Y-%m-%dT%H:%M:%S")
        else:
            dev_exp = None

        dev_rank = r.get('value') if r is not None else None
        # dev_variants = v.text if v is not None else None
        variants_isdefault = v.find('.//IsDefault[@value]')
        dev_variants = v.find('.//SPS//Value[@locale="en"]')
        variants_isdefault = variants_isdefault.get('value')
        dev_variants = dev_variants.text
        variants_ofid = v.find('.//SPS//UniqueFields//Field[@name="ProductOfferingID"]')
        variants_ofid = variants_ofid.get('value')
        # print(variants_ofid)
        variants_prid = v.find('.//SPS//UniqueFields//Field[@name="ProductSpecID"]')
        variants_prid = variants_prid.get('value')
        devid = variants_ofid + '_' + variants_prid
        # print(variants_prid)
        variants_cid = v.find('.//SPS//UniqueFields//Field[@name="ID"]')
        variants_cid = variants_cid.get('value')

        print("\ninserting data for VG - " + dev_name_en + " and SPS - " + dev_variants)
        cur.execute(
            "insert into VARIANTGROUPS(VG_ID,VG_NAME_EN,VG_NAME_IT,VG_CODE,VG_SALES_EFF_DT,VG_SALES_EXP_DT,VG_DESC,VG_RANK,VG_SPS_VARIANT,VG_SPS_IS_DEFAULT,VARIANT_CID,DEVICE_ID,DISTRIB_FILE_NAME,RUN_BY,JOB_RUN_TIME) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)",
            [dev_id, dev_name_en, dev_name_it, dev_code, dev_eff, dev_exp, dev_desc, dev_rank, dev_variants,
             variants_isdefault, variants_cid, devid, zipfilename, username, now])

conn.commit()

for g in root.xpath('.//VariantGroup'):
    name_EN = g.find('.//Name/Value[@locale="en"]')
    name_IT = g.find('.//Name/Value[@locale="it"]')
    VG_ID = g.find('.//VariantGroupVersion/ID[@value]')
    VG_Code = g.find('.//VariantGroupVersion//Code[@value]')
    desc = g.find('.//Description/Value[@locale="it"]')
    sed = g.find('.//VariantGroupVersion/SaleEffectiveDate[@value]')
    sexd = g.find('.//VariantGroupVersion/SaleExpirationDate[@value]')
    r = g.find('.//RecommendationRank//RecommendationRank[@value]')
    attrs = g.findall('.//Attributes//ProductAttributeRelation')

    for v in attrs:
        dev_name_en = name_EN.text if name_EN is not None else None
        dev_name_it = name_IT.text if name_IT is not None else None
        dev_id = VG_ID.get('value') if VG_ID is not None else None
        dev_code = VG_Code.get('value') if VG_Code is not None else None
        dev_desc = desc.get('value') if desc is not None else None

        dev_eff = sed.get('value') if sed is not None else None

        if dev_eff is not None:
            dev_eff = datetime.strptime(dev_eff, "%Y-%m-%dT%H:%M:%S")
        else:
            dev_eff = None
        dev_exp = sexd.get('value') if sexd is not None else None
        if dev_exp is not None:
            dev_exp = datetime.strptime(dev_exp, "%Y-%m-%dT%H:%M:%S")
        else:
            dev_exp = None

        dev_rank = r.get('value') if r is not None else None
        # dev_variants = v.text if v is not None else None
        attr_name = v.find('.//AssignableAttribute//Name//Value[@locale="en"]')
        attr_names = attr_name.text if attr_name is not None else None
        # print(attr_names)
        attr_code = v.find('.//AssignableAttribute//UniqueFields//Field[@name="Code"]')
        attr_codes = attr_code.get('value') if attr_code is not None else None
        # print(attr_codes)
        attr_id = v.find('.//AssignableAttribute//UniqueFields//Field[@name="ID"]')
        attr_ids = attr_id.get('value') if attr_id is not None else None
        # print(attr_ids)

        def_value = v.find('.//DefaultValue[@value]')
        def_values = def_value.get('value') if def_value is not None else None
        # print(def_values)

        constant = v.find('.//Constant[@value]')
        constants = constant.get('value') if constant is not None else None
        # print(constants)

        useashighlight = v.find('.//UseAsHighlight[@value]')
        useashighlights = useashighlight.get('value') if useashighlight is not None else None
        # print(useashighlights)

        useasvariant = v.find('.//UseAsVariant[@value]')
        useasvariants = useasvariant.get('value') if useasvariant is not None else None
        # print(useasvariants)

        print("\n\ninserting data for VG - " + dev_name_en + " and attribute - " + attr_names)
        cur.execute(
            "insert into VARIANTGROUP_ATTRS(VG_ID,VG_NAME_EN,VG_NAME_IT,VG_CODE,VG_SALES_EFF_DT,VG_SALES_EXP_DT,VG_DESC,VG_RANK,VG_ATTRIB_NAME,VG_ATTRIB_CODE,VG_ATTRIB_ID,DEFAULT_VALUE,CONSTANT,USE_AS_HIGHLIGHT,USE_AS_VARIANT,DISTRIB_FILE_NAME,RUN_BY,JOB_RUN_TIME) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18)",
            [dev_id, dev_name_en, dev_name_it, dev_code, dev_eff, dev_exp, dev_desc, dev_rank, attr_names, attr_codes,
             attr_ids, def_values, constants, useashighlights, useasvariants, zipfilename, username, now])

print("\n\nTable VARIANTGROUPS is populated.")
print("\n\nTable VARIANTGROUP_ATTRS is populated.")

conn.commit()

print("\n\nChanges in DB were committed")

rs = cur.execute("select count(*) from variantgroups")

for row in rs:
    print(str(row[0]) + ' rows were inserted.')

rs = cur.execute(
    "select count(distinct VG_ID) from variantgroups where ( trunc(VG_SALES_EXP_DT)>=trunc(SYSDATE) or VG_SALES_EXP_DT IS NULL)")

for row in rs:
    print('Count of Non-Expired Variant Groups - ' + str(row[0]))

rs = cur.execute(
    "update variantgroups a set sku = (select distinct default_value from tbitem_property where property_id = '17380' and cid = a.VARIANT_CID)")

conn.commit()

print("\n\nExiting..\n\n")
print("Have a good day ahead and take care.. :)" + bcolors.RESET)

cur.close()
conn.close()