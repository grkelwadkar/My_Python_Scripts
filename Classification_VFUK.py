from lxml import etree
import os
import cx_Oracle


user = 'system'
pwd = 'system'
host = 'localhost'
port = '1521'
instance = 'XE'


dsn_tns = cx_Oracle.makedsn(host, port, instance)

conn = cx_Oracle.connect(user=user, password=pwd, dsn=dsn_tns)

cur = conn.cursor()

print('\n\nConnected to ' + user + '@' + instance)


rs = cur.execute("select count(*) from ALL_TABLES where table_name = 'CLASSIFICATION_REL'")

for row in rs:
    cnt = row[0]

if (cnt == 1):
    cur.execute('DROP TABLE CLASSIFICATION_REL')
    print('\n\nDropped table CLASSIFICATION_REL')

    cur.execute('''
   CREATE TABLE CLASSIFICATION_REL (
   CLASSIFICATION_NAME VARCHAR2(500),
   CLASSIFICATION_ID VARCHAR2(500),
   CLASSIFICATION_DESC VARCHAR2(500),
   CLASSIFICATION_CODE VARCHAR2(500),
   RELATION_ID VARCHAR2(500),
   RELATED_TYPE VARCHAR2(500), 
   RELATION_NAME VARCHAR2(500),
   ACTION_NAME VARCHAR2(500),
   REL_PROD_CRITERIA_NAME VARCHAR2(500),
   REL_PROD_CRITERIA_DESC VARCHAR2(500),
   RPC_PARENT_CAT_COND_LEFT VARCHAR2(500),
   RPC_PARENT_CAT_COND_OPERATOR VARCHAR2(500),
    RPC_PARENT_CAT_COND_RIGHT VARCHAR2(500),
    RPC_CHILD_CAT_COND_CATEGORY VARCHAR2(500),
    RPC_CHILD_CAT_COND_LEFT VARCHAR2(500),
    RPC_CHILD_CAT_COND_OPERATOR VARCHAR2(500),
    RPC_CHILD_CAT_COND_RIGHT VARCHAR2(500)
   )''')

    print('\n\nCreated TABLE CLASSIFICATION_REL')
else:
    cur.execute('''
       CREATE TABLE CLASSIFICATION_REL (
       CLASSIFICATION_NAME VARCHAR2(500),
       CLASSIFICATION_ID VARCHAR2(500),
       CLASSIFICATION_DESC VARCHAR2(500),
       CLASSIFICATION_CODE VARCHAR2(500),
       RELATION_ID VARCHAR2(500),
       RELATED_TYPE VARCHAR2(500), 
       RELATION_NAME VARCHAR2(500),
       ACTION_NAME VARCHAR2(500),
       REL_PROD_CRITERIA_NAME VARCHAR2(500),
       REL_PROD_CRITERIA_DESC VARCHAR2(500),
       RPC_PARENT_CAT_COND_LEFT VARCHAR2(500),
       RPC_PARENT_CAT_COND_OPERATOR VARCHAR2(500),
        RPC_PARENT_CAT_COND_RIGHT VARCHAR2(500),
        RPC_CHILD_CAT_COND_CATEGORY VARCHAR2(500),
        RPC_CHILD_CAT_COND_LEFT VARCHAR2(500),
        RPC_CHILD_CAT_COND_OPERATOR VARCHAR2(500),
        RPC_CHILD_CAT_COND_RIGHT VARCHAR2(500)
       )''')

    print('\n\nCreated TABLE CLASSIFICATION_REL')


file = r'C:\Users\grkel\Desktop\Classification.xml'

root = etree.parse(file)


for g in root.xpath('.//Classification'):
    class_name = g.find('.//Name//Value[@locale="en"]')
    class_name = class_name.text if class_name is not None else None

    print('\n' + class_name)


    if class_name == 'Plan':
        class_ID = g.find('.//ClassificationVersions//ClassificationVersion//ID[@value]')
        class_ID = class_ID.get('value') if class_ID is not None else None
        print(class_ID)

        class_description = g.find('.//ClassificationVersions//ClassificationVersion//Description//Value[@locale="en"]')
        class_description = class_description.get('value') if class_description is not None else None
        print(class_description)

        class_code = g.find('.//ClassificationVersions//ClassificationVersion//Code[@value]')
        class_code = class_code.get('value') if class_code is not None else None
        print(class_code)

        ordcat2ordcatrels = g.findall('.//ClassificationVersions//ClassificationVersion//OrderingCategoryToCategoryRelation//OrderingCategoryToCategoryRelation')

        #print(ordcat2ordcatrels)

        for ordcat2ordcatrel in ordcat2ordcatrels:
            rel_id = ordcat2ordcatrel.find('.//ID[@value]')
            rel_id = rel_id.get('value') if rel_id is not None else None
            #print(rel_id)

            related_type = ordcat2ordcatrel.find('.//Related_Type//Name//Value[@locale="en"]')
            related_type = related_type.text if related_type is not None else None
            #print(related_type)

            relation_name = ordcat2ordcatrel.find('.//RelationName//Value[@locale="en"]')
            relation_name = relation_name.get('value') if relation_name is not None else None
            #print(relation_name)

            action_name = ordcat2ordcatrel.find('.//ActionName//Value[@locale="en"]')
            action_name = action_name.get('value') if action_name is not None else None
            #print(action_name)

            rp_criterias = ordcat2ordcatrel.findall('.//CompatibilityCriterion//RelatedProductCriteria')


            for rp_criteria in rp_criterias:
                rpc_name = rp_criteria.find('.//Name/Value[@locale="en"]')
                rpc_name = rpc_name.get('value') if rpc_name is not None else None
                #print(rpc_name)


                rpc_description = rp_criteria.find('.//Description//Value[@locale="en"]')
                rpc_description = rpc_description.get('value') if rpc_description is not None else None
                #print(rpc_description)


                rpc_parent_cat_cond_left =  rp_criteria.find('.//ParentCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//LeftOperand//RelatedProductLeftOperand//Attribute//Name//Value[@locale="en"]')
                rpc_parent_cat_cond_left = rpc_parent_cat_cond_left.text if rpc_parent_cat_cond_left is not None else None
                #print(rpc_parent_cat_cond_left)

                rpc_parent_cat_cond_operator = rp_criteria.find('.//ParentCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//Operator//Name//Value[@locale="en"]')
                rpc_parent_cat_cond_operator = rpc_parent_cat_cond_operator.text if rpc_parent_cat_cond_operator is not None else None
                #print(rpc_parent_cat_cond_operator)

                rpc_parent_cat_cond_right = rp_criteria.find('.//ParentCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//RightOperator//RelatedProductRightOperand//Value//Value')
                rpc_parent_cat_cond_right = rpc_parent_cat_cond_right.get('value') if rpc_parent_cat_cond_right is not None else None
                #print(rpc_parent_cat_cond_right)

                rpc_child_cat_cond_category = rp_criteria.find(
                    './/ChildCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//LeftOperand//RelatedProductLeftOperand//Category//Name//Value[@locale="en"]')
                rpc_child_cat_cond_category = rpc_child_cat_cond_category.text if rpc_child_cat_cond_category is not None else None
                #print(rpc_child_cat_cond_category)

                rpc_child_cat_cond_left = rp_criteria.find(
                    './/ChildCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//LeftOperand//RelatedProductLeftOperand//Attribute//Name//Value[@locale="en"]')
                rpc_child_cat_cond_left = rpc_child_cat_cond_left.text if rpc_child_cat_cond_left is not None else None
                #print(rpc_child_cat_cond_left)

                rpc_child_cat_cond_operator = rp_criteria.find(
                    './/ChildCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//Operator//Name//Value[@locale="en"]')
                rpc_child_cat_cond_operator = rpc_child_cat_cond_operator.text if rpc_child_cat_cond_operator is not None else None
                #print(rpc_child_cat_cond_operator)

                rpc_child_cat_cond_right = rp_criteria.find(
                    './/ChildCategoryConditions//RelatedProductCondition//Expressions//RelatedProductExpression//RightOperator//RelatedProductRightOperand//Value//Value')
                rpc_child_cat_cond_right = rpc_child_cat_cond_right.get('value') if rpc_child_cat_cond_right is not None else None
                print(rpc_child_cat_cond_right)

                cur.execute(
                    "insert into OFFERING_ATTRIBUTE_RELATION (CLASSIFICATION_NAME,CLASSIFICATION_ID,CLASSIFICATION_DESC,CLASSIFICATION_CODE,RELATION_ID,RELATED_TYPE, RELATION_NAME,ACTION_NAME,REL_PROD_CRITERIA_NAME,REL_PROD_CRITERIA_DESC,RPC_PARENT_CAT_COND_LEFT,RPC_PARENT_CAT_COND_OPERATOR, RPC_PARENT_CAT_COND_RIGHT, RPC_CHILD_CAT_COND_CATEGORY, RPC_CHILD_CAT_COND_LEFT, RPC_CHILD_CAT_COND_OPERATOR, RPC_CHILD_CAT_COND_RIGHT) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16, :17)",
                    [class_name, class_ID, class_description, class_code, rel_id, related_type, relation_name, action_name,
                     rpc_name, rpc_description, rpc_parent_cat_cond_left, rpc_parent_cat_cond_operator, rpc_parent_cat_cond_right, rpc_child_cat_cond_category, rpc_child_cat_cond_left,rpc_child_cat_cond_operator,rpc_child_cat_cond_right])





conn.commit()
cur.close()
conn.close()