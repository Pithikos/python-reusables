'''
Gives back an xpath that points to given element and only

Parameters:   
    element  -  an lxml element object

Output:
    xpath    -  an xpath string that points to the given element and only

'''
def get_element_xpath(element):

    xpath = ''
    
    def element_tag(el):
        tag = el.tag
        if '{' and '}' in tag:
            splut = tag.split('}')
            if len(splut)==2:
                return splut[1]
            else:
                print("ERROR: Element tag is in unknown format ('%s')" % tag)
                return None
        else:
            return tag

    def same_tag_siblings(element):
        parent = element.getparent()
        if parent is not None:
            return filter(lambda el: element_tag(el) == element_tag(element), parent.getchildren())
        else:
            return [element]

    while (element is not None):
        twins = same_tag_siblings(element)
        print(twins)
        index = twins.index(element) if len(twins)>0 else 0
        if len(twins)==1:
            xpath = '/%s' % element_tag(element) + xpath
        else:
            xpath = '/%s[%d]' % (element_tag(element), index+1) + xpath
        element = element.getparent()

    return '/' + xpath




################################ EXAMPLE ###############################


from selenium import webdriver
from lxml import etree

browser = webdriver.Chrome()
browser.get('http://www.google.com')
html = etree.HTML(browser.page_source)


# Get xpath of the Google Search button
button = html.xpath('//input[@value="Google Search"]')[0]
print(get_element_xpath(button)) # --> //html/body/div[1]/div[3]/form/div[2]/div[3]/center/input[1]
