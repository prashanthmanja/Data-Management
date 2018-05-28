import sys
from lxml import html
from lxml import etree
from xml.etree.ElementTree import SubElement

#inputfile = open(sys.argv[1])
inputfile=open('result9.html')
#outputfile=open(sys.argv[2],'w')
outputfile=open('result9.xml','w')
data = inputfile.read()
htree = html.etree.HTML(data)

no_of_books=htree.xpath('//div[contains(@id,"result")]//h2/@data-attribute')
authors = htree.xpath('//div[contains(@class,"a-row a-spacing-small")]/div[2]//span[contains(@class,"a-size-small a-color-secondary")]//text()')
root = etree.Element('books')
for i in range(len(no_of_books)):
    book = SubElement(root, "book")
    title=SubElement(book,"title")
    title.text=htree.xpath('//div[contains(@class,"a-row a-spacing-small")]//h2/@data-attribute')[i]
    publication_date=SubElement(book,"pubilcation_date")
    publication_date.text=htree.xpath('//div[contains(@class,"a-row a-spacing-small")]/div[//h2][1]/span[contains(@class,"a-size-small a-color-secondary")][1]/text()')[i]
    no_of_authors=len(htree.xpath('//div[contains(@class,"a-row a-spacing-small")]/div[2]')[i])
    k =len(authors)
    if authors[0]=='by ' and len(authors)>=3 and authors[1].endswith(" and "):
                author = SubElement(book, "author")
                author.text=authors[1][:-4]
                author = SubElement(book, "author")
                author.text = authors[2]
                del authors[0:3]
    elif authors[0]=='by ' and len(authors)>=4 and authors[2]==' and ':
                author = SubElement(book, "author")
                author.text = authors[1]
                author = SubElement(book, "author")
                author.text = authors[3]
                del authors[0:4]
    elif authors[0]=='by ':
                author = SubElement(book, "author")
                author.text = authors[1]
                del authors[0:2]
output = etree.tostring(root, pretty_print=True)
print output
outputfile.write(output)

