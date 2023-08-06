#!/usr/bin/env python3

import sys, re, os, libxml2, xml.parsers.expat

from collections import namedtuple

XML = namedtuple('XML', ['doc','ctx','nsp'])

class NamespaceParser(object):
	'''
	obtain xmlns namespace prefix and urls
	'''

	def __init__(self, encoding=None):
		self.nsp = dict()
		self.done = False
		self.parser = xml.parsers.expat.ParserCreate(encoding=encoding)
		self.parser.StartElementHandler	= self.startElementHandler

	def startElementHandler(self, name, attrs):
		if not self.done:
			for name, value in attrs.items():
				if name.startswith('xmlns:'):
					prefix = name.split(':')[-1]
					self.nsp[prefix] = value
			self.done = True

			
def getContextFromStringWithNS(xml, argsNS=None, urls=None):

	parser = NamespaceParser()
	parser.parser.Parse(xml)
	
	def handler(ectx, error):
		sys.stderr.write('error=%s'%error)

	libxml2.registerErrorHandler(handler,'')

	doc = libxml2.parseDoc(xml)
	ctx = doc.xpathNewContext()
	nsp = parser.nsp

	for p, n in nsp.items():
		nsp[p] = n
		if urls:
			sys.stderr.write('xmlns:%s=%s\n'%(p, n))

	if argsNS:
		pn = re.compile('^([^=]*)=["\']([^\'"]*)["\']$')
		for ns in argsNS:
			mn = pn.match(ns)
			if mn:
				nsp[mn.group(1)] = mn.group(2)

	for prefix, namespace in nsp.items():
		ctx.xpathRegisterNs(prefix,namespace)

	return (doc,ctx,nsp)

def getContextFromString(xml, argsNS=None, urls=None):
	(doc,ctx,nsp) = getContextFromStringWithNS(xml, argsNS, urls)
	return (doc,ctx,nsp)

def getContextFromFile(fn, argsNS=None, urls=None):
	fp = open(fn)
	xml = fp.read()
	fp.close()
	return getContextFromString(xml, argsNS, urls)

def getContextFromStream(input, argsNS=None, urls=None):
	xml = input.read()
	return getContextFromString(xml, argsNS, urls)

def getElements(context,xpath,parent=None):
	if parent:
		context.setContextNode(parent)
	return context.xpathEval(xpath)

def getElement(context,xpath,parent=None):
	elements = getElements(context,xpath,parent)
	if len(elements) > 0:
		return elements[0]
	return None

def getElementText(context,xpath,parent=None):
	element = getElement(context,xpath,parent)
	if element:
		return element.content
	return None

def setElementText(context,xpath,value,parent=None):
	element = getElement(context,xpath,parent)
	if element:
		element.setContent(value)
	return

def insertElement(document, name, before, parent=None, ns=None):
	if not parent:
		parent = document.getRootElement()
	#print(parent.ns(), type(parent.ns()))
	element = document.newDocNode(ns or parent.ns(), name, None)
	before.addPrevSibling(element)
	return element

def appendElement(document, name, after, parent=None, ns=None):
	if not parent:
		parent = document.getRootElement()
	#print(parent.ns(), type(parent.ns()))
	element = document.newDocNode(ns or parent.ns(), name, None)
	after.addNextSibling(element)
	return element

def addElement(document, name, parent=None, ns=None):
	if not parent:
		parent = document.getRootElement()
	#print(parent.ns(), type(parent.ns()))
	element = document.newDocNode(ns or parent.ns(), name, None)
	parent.addChild(element)
	return element

def addElementText(document, name, value, parent=None, ns=None):
	if not parent:
		parent = document.getRootElement()
	element = document.newDocNode(ns or parent.ns(),name,value)
	parent.addChild(element)
	return element

def addElementCDATA(document,name,value,parent=None):
	element = addElement(document,name,parent=parent)
	cdata = document.newCDataBlock(value,len(value))
	element.addChild(cdata)
	return element

def hasAttribute(element,attname):
	return element.hasProp(attname)

def getAttribute(element,attname):
	return element.prop(attname)

def setAttribute(element,attname,value):
	try:
		element.setProp(attname,value)
	except:
		element.newProp(attname,value)
	return

def delAttribute(element, attname):
	'''
	property = getElement(ctx, '@ref', element)
	property.unlinkNode()
	property.freeNode()
	'''
	return

