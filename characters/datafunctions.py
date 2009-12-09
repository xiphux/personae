from personae.characters.models import Attribute, AttributeChoice, AttributeIntegerValue, AttributeStringValue, AttributeTextValue, AttributeChoiceValue

#
# Build attribute list
# universe_attributes: list of universe attributes to build data for
# revision: revision with data
#
def buildattributelist(universe_attributes, revision):
	attribute_list = {}

	univ_attributes_readlist = universe_attributes.filter(parentattribute__isnull=True)

	for attr in univ_attributes_readlist:
		val = readattribute(attr, revision)
		if val is not None:
			attribute_list[attr.descriptor] = val
	
	return attribute_list

#
# read attribute
# attr: attribute to read data for
# revision: revision with data
#
def readattribute(attr, revision):
	if attr.type == 1:
		attrvaluelist = revision.attributeintegervalue_set.all()
	elif attr.type == 2:
		attrvaluelist = revision.attributestringvalue_set.all()
	elif attr.type == 3:
		attrvaluelist = revision.attributetextvalue_set.all()
	elif attr.type == 4:
		attrvaluelist = revision.attributechoicevalue_set.all()
	elif attr.type == 5:
		attrvaluelist = revision.attributesetvalue_set.all()
	else:
		return

	if attr.type == 5:
		if attr.multiple:
			vallist = attrvaluelist.filter(attribute=attr.id).order_by('line')
			val = {}
			data_lists = {}
			for subattr in attr.attribute_set.all():
				data_lists[subattr.descriptor] = readattribute(subattr, revision)
			for valitem in vallist:
				val[valitem.line] = {}
				for subattr in attr.attribute_set.all():
					try:
						tmp = data_lists[subattr.descriptor][valitem.line]
						val[valitem.line][subattr.descriptor] = tmp
					except (IndexError, KeyError):
						pass
			return val
		else:
			subattr_values = {}
			for subattr in attr.attribute_set.all():
				val = readattribute(subattr, revision)
				if val is not None:
					subattr_values[subattr.descriptor] = val
			if len(subattr_values) > 0:
				return subattr_values
	else:
		try:
			if attr.multiple:
				vallist = attrvaluelist.filter(attribute=attr.id).order_by('line')
				val = {}
				for valitem in vallist:
					val[valitem.line] = valitem
			else:
				val = attrvaluelist.get(attribute=attr.id)
			return val
		except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
			pass

#
# save attribute set
# attr: attribute of type set
# postdata: POST data dictionary
# newrevision: new revision to save to
# oldrevision: old revision to copy forward from
#
def saveattributeset(attr, postdata, newrevision, oldrevision):
	vallist = {}
	maxlines = 0
	for subattr in attr.attribute_set.all():
		data = postdata.getlist(subattr.descriptor)
		if len(data) > maxlines:
			maxlines = len(data)
		vallist[subattr.descriptor] = data
	
	for i in range(maxlines):
		newvallist = []
		for subattr in attr.attribute_set.all():
			try:
				val = savesingleattribute(subattr, i+1, vallist[subattr.descriptor][i], newrevision, oldrevision)
				if val is not None:
					newvallist.append(val)
			except (IndexError, KeyError):
				pass
		if len(newvallist) > 0:
			needsnew = False
			if oldrevision is None:
				needsnew = True
			else:
				for item in newvallist:
					if item.attributesetvalue.count() == 0:
						needsnew = True
			if needsnew == True:
				setattr = newrevision.attributesetvalue_set.create(attribute=attr, line=i+1)
				for item in newvallist:
					item.attributesetvalue.add(setattr)
					item.save()
			else:
				setattr = oldrevision.attributesetvalue_set.get(attribute=attr, line=i+1)
				setattr.revisions.add(newrevision)
				setattr.save()

#
# save attribute
# attr: attribute to save
# postdata: POST data dictionary
# newrevision: new revision to save to
# oldrevision: old revision to copy forward from
#
def saveattribute(attr, postdata, newrevision, oldrevision):
	if attr.multiple == True:
		try:
			vallist = postdata.getlist(attr.descriptor)
		except (KeyError):
			return

		if len(vallist) == 0:
			return
		
		count = 0
		for ln in vallist:
			val = ln
			if len(val) == 0:
				continue

			if attr.type == 1 or attr.type == 4:
				val = int(val)
				if val < 1:
					continue

			count += 1
			savesingleattribute(attr, count, val, newrevision, oldrevision)

				
	else:
		try:
			val = postdata[attr.descriptor]
		except (KeyError):
			return

		savesingleattribute(attr, 0, val, newrevision, oldrevision)

#
# save single line of attribute
# attr: attribute to save
# line: line of data to save
# data: data to save
# newrevision: new revision to save to
# oldrevision: old revision to copy forward from
#
def savesingleattribute(attr, line, data, newrevision, oldrevision):
	if line < 0:
		return

	val = data

	if len(val) == 0:
		return

	if attr.type == 1 or attr.type == 4:
		val = int(val)
		if val < 1:
			return

	if attr.type == 1:
		if oldrevision is not None:
			oldattrset = oldrevision.attributeintegervalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributeintegervalue_set
	elif attr.type == 2:
		if oldrevision is not None:
			oldattrset = oldrevision.attributestringvalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributestringvalue_set
	elif attr.type == 3:
		if oldrevision is not None:
			oldattrset = oldrevision.attributetextvalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributetextvalue_set
	elif attr.type == 4:
		if oldrevision is not None:
			oldattrset = oldrevision.attributechoicevalue_set
		else:
			oldattrset = None
		newattrset = newrevision.attributechoicevalue_set
	else:
		return

	if oldrevision is not None:
		try:
			oldval = oldattrset.get(attribute=attr, line=line)
			if attr.type == 4:
				if oldval.choice.id == val:
					oldval.revisions.add(newrevision)
					oldval.save()
					return oldval
			else:
				if oldval.value == val:
					oldval.revisions.add(newrevision)
					oldval.save()
					return oldval
		except (AttributeIntegerValue.DoesNotExist, AttributeStringValue.DoesNotExist, AttributeTextValue.DoesNotExist, AttributeChoiceValue.DoesNotExist):
			pass
	if attr.type == 4:
		ch = AttributeChoice.objects.get(pk=val)
		return newattrset.create(attribute=attr, choice=ch, line=line)
	else:
		return newattrset.create(attribute=attr, value=val, line=line)


