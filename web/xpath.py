'''
Gives back an xpath that points to given element and only

Takes:
  element  -  an lxml element object

Returns:
  xpath    -  an xpath string that points to the given element and only
'''
def get_element_xpath(element):

    xpath = ''
    
    def element_tag(el):
        splut = el.tag.split('}')
        if len(splut)==2:
            return splut[1]
        else:
            print("ERROR: Element tag is in unknown format ('%s')" % el.tag)
            return None

    def same_tag_siblings(element):
        parent = element.getparent()
        if parent is not None:
            return filter(lambda el: el.tag == element.tag, parent.getchildren())
        else:
            return []

    while (element is not None):
        twins  = same_tag_siblings(element)
        index = twins.index(element) if len(twins)>0 else 0
        if index == 0:
            xpath = '/%s' % element_tag(element) + xpath
        else:
            xpath = '/%s[%d]' % (element_tag(element), index+1) + xpath
        element = element.getparent()

    return '/' + xpath
