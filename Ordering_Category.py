#!/usr/bin/env python
# encoding: utf-8

from lxml import etree
import cx_Oracle

file = r'C:\Users\grkel\Desktop\Category.xml'

root = etree.parse(file)

for g in root.xpath('.//OrderingCategory'):
    name_EN = g.find('.//Name//Value[@locale="en"]')
    name_EN = name_EN.text if not None else None
    print("Ordering Category Name is -----" + name_EN)


    cat_id = g.find('.//OrderingCategoryVersion//ID')
    cat_id = cat_id.get('value') if not None else None
    print("Ordering Category ID is ---" + cat_id)

    cat_code = g.find('.//OrderingCategoryVersion//Code')
    cat_code = cat_code.get('value') if not None else None
    print("Ordering Category Code is ---" + cat_code)


    relatedProducts = g.findall('.//OrderingCategoryVersion//RelatedProducts')
    #print(relatedProducts)

    if len(relatedProducts) != 0:
        print('relatedProducts '+'---->')
        for elems in relatedProducts:
            elementIDs = elems.findall('.//ElementId')
            for e in elementIDs:
                elemName = e.find('.//Name//Value[@locale="en"]')
                elemName = elemName.text if not None else None
                print(elemName)

                elemID = e.find('.//UniqueFields//Field[@name="ID"]')
                elemID = elemID.get('value') if elemID is not None else None
                #print(elemID)

                elemCode = e.find('.//UniqueFields//Field[@name="Code"]')
                elemCode = elemCode.get('value') if elemCode is not None else None
                #print(elemCode)

                elemProductSpecID = e.find('.//UniqueFields//Field[@name="ProductSpecID"]')
                elemProductSpecID = elemProductSpecID.get('value') if elemProductSpecID is not None else None
                #print(elemProductSpecID)

                elemProductOfferingID = e.find('.//UniqueFields//Field[@name="ProductOfferingID"]')
                elemProductOfferingID = elemProductOfferingID.get('value') if elemProductOfferingID is not None else None
                #print(elemProductOfferingID)

    relatedOffers = g.findall('.//OrderingCategoryVersion//RelatedProductOfferings')
    # print(relatedProducts)

    if len(relatedOffers) != 0:
        print('relatedOffers ' + '---->')
        for elems in relatedOffers:
            elementIDs = elems.findall('.//ElementId')
            for e in elementIDs:
                elemName = e.find('.//Name//Value[@locale="en"]')
                elemName = elemName.text if not None else None
                print(elemName)

                elemID = e.find('.//UniqueFields//Field[@name="ID"]')
                elemID = elemID.get('value') if elemID is not None else None
                #print(elemID)

                elemCode = e.find('.//UniqueFields//Field[@name="Code"]')
                elemCode = elemCode.get('value') if elemCode is not None else None
                #print(elemCode)

    relatedPrices = g.findall('.//OrderingCategoryVersion//RelatedPrice')
    # print(relatedProducts)

    if len(relatedPrices) != 0:
        print('relatedPrices'+'--->')
        for elems in relatedPrices:
            elementIDs = elems.findall('.//ElementId')
            for e in elementIDs:
                elemName = e.find('.//Name//Value[@locale="en"]')
                elemName = elemName.text if not None else None
                print(elemName)

                elemID = e.find('.//UniqueFields//Field[@name="ID"]')
                elemID = elemID.get('value') if elemID is not None else None
                #print(elemID)

                elemCode = e.find('.//UniqueFields//Field[@name="Code"]')
                elemCode = elemCode.get('value') if elemCode is not None else None
                #print(elemCode)