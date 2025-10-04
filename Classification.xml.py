#!/usr/bin/env python
# encoding: utf-8

from lxml import etree
import cx_Oracle

file = r'C:\Users\grkel\Desktop\Classification.xml'

root = etree.parse(file)

for g in root.xpath('.//Classification'):
    name_EN = g.find('.//Name//Value[@locale="en"]')
    name_EN = name_EN.text if not None else None
    print("Classification Name is -----" + name_EN)

    class_id = g.find('.//ClassificationVersions//ClassificationVersion//ID')
    class_id = class_id.get('value') if not None else None
    print("Classification ID is ---" + class_id)

    class_code = g.find('.//ClassificationVersions//ClassificationVersion//Code')
    class_code = class_code.get('value') if not None else None
    print("Classification Code is ---" + class_code)


    relClassName = g.find('.//ClassificationVersions//ClassificationVersion//OrderingCategoryToCategoryRelation//OrderingCategoryToCategoryRelation//Category//ElementId//Name//Value[@locale="en"]')

    if relClassName is not None:
        relClassName = relClassName.text if not None else None
        print(relClassName)

    relClassID = g.find(
        './/ClassificationVersions//ClassificationVersion//OrderingCategoryToCategoryRelation//OrderingCategoryToCategoryRelation//Category//ElementId//UniqueFields//Field[@name="ID"]')


    if relClassID is not None:
        relClassID = relClassID.get('value') if not None else None
        print(relClassID)

    relatedProdCriteria = g.findall('.//ClassificationVersions//ClassificationVersion//OrderingCategoryToCategoryRelation//OrderingCategoryToCategoryRelation//CompatibilityCriterion//RelatedProductCriteria')

    if len(relatedProdCriteria) != 0:
        for relName in relatedProdCriteria:
            #print(relName)

            relName_nm = relName.find('.//Name//Value[@locale="en"]')
            relName_nm = relName_nm.get('value') if relName_nm is not None else None
            print(relName_nm)

            ChildCategoryConditions = relName.findall('.//ChildCategoryConditions//RelatedProductCondition//RelatedBasePlan//ElementId')
            #print('ChildCategoryConditions' , ChildCategoryConditions)

            for elem in ChildCategoryConditions:
                elem_plan_name = elem.find('.//Name/Value[@locale="en"]')
                elem_plan_name = elem_plan_name.text if elem_plan_name is not None else None
                print(elem_plan_name)

                elem_plan_ID = elem.find('.//UniqueFields//Field[@name="ID"]')
                elem_plan_ID = elem_plan_ID.get('value') if elem_plan_ID is not None else None
                print(elem_plan_ID)

                elem_plan_code = elem.find('.//UniqueFields//Field[@name="Code"]')
                elem_plan_code = elem_plan_code.get('value') if elem_plan_code is not None else None
                print(elem_plan_code)

                ParentCategoryConditions = relName.findall(
                    './/ParentCategoryConditions//RelatedProductCondition//RelatedProducts//ElementId')

                print(ParentCategoryConditions)

                for el in ParentCategoryConditions:
                    el_dev_name = el.find('.//Name//Value[@locale="en"]')
                    el_dev_name = el_dev_name.text if el_dev_name is not None else None
                    print(el_dev_name)

                    elem_dev_ID = el.find('.//UniqueFields//Field[@name="ID"]')
                    elem_dev_ID = elem_dev_ID.get('value') if elem_dev_ID is not None else None
                    print(elem_dev_ID)

                    elem_dev_code = el.find('.//UniqueFields//Field[@name="Code"]')
                    elem_dev_code = elem_dev_code.get('value') if elem_dev_code is not None else None
                    print(elem_dev_code)

                    elem_dev_prod = el.find('.//UniqueFields//Field[@name="ProductSpecID"]')
                    elem_dev_prod = elem_dev_prod.get('value') if elem_dev_prod is not None else None
                    print(elem_dev_prod)

                    elem_dev_offer = el.find('.//UniqueFields//Field[@name="ProductOfferingID"]')
                    elem_dev_offer = elem_dev_offer.get('value') if elem_dev_offer is not None else None
                    print(elem_dev_offer)
