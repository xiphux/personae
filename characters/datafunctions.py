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

	for i in range(1, maxlines+1):
		newvallist = []
		for subattr in attr.attribute_set.all():
			try:
				val = savesingleattribute(subattr, i, vallist[subattr.descriptor][i-1], newrevision, oldrevision)
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
				setattr = newrevision.attributesetvalue_set.create(attribute=attr, line=i)
				for item in newvallist:
					item.attributesetvalue.add(setattr)
					item.save()
			else:
				setattr = oldrevision.attributesetvalue_set.get(attribute=attr, line=i)
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

	if len(str(val)) == 0:
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

#
# diff two revisions
# leftrev: left revision
# rightrev: right revision
#
def diffrevisions(leftrev, rightrev):
	if (leftrev is None) or (rightrev is None):
		return

	if leftrev.character.universe != rightrev.character.universe:
		return

	try:
		universe_attributes = leftrev.character.universe.attribute_set.all()
	except:
		return

	difflist = []
	for attr in universe_attributes:
		if attr.type != 5:
			leftattr = readattribute(attr, leftrev)
			rightattr = readattribute(attr, rightrev)
			diff = diffattribute(attr, leftattr, rightattr)
			if diff is not None:
				difflist.append(diff)

	return difflist

#
# diff attribute
# attr: attribute to diff
# leftvalue: left item or list of items
# rightvalue = right item or list of items
#
def diffattribute(attr, leftvalue, rightvalue):
	if (leftvalue is None) and (rightvalue is None):
		return

	if attr.multiple:
		listlen = len(leftvalue)
		values = {}
		if len(rightvalue) > listlen:
			listlen = len(rightvalue)
		for i in range(1, listlen+1):
			leftline = None
			rightline = None
			try:
				leftline = leftvalue[i]
			except (KeyError):
				pass
			try:
				rightline = rightvalue[i]
			except (KeyError):
				pass

			if (leftline is None) and (rightline is None):
				continue

			if attr.type == 4:
				if (leftline is None) or (rightline is None):
					values[i] = (leftline, rightline)
				elif leftline.choice != rightline.choice:
					values[i] = (leftline, rightline)
			elif (attr.type == 1) or (attr.type == 2) or (attr.type == 3):
				if (leftline is None) or (rightline is None):
					values[i] = (leftline, rightline)
				elif leftline.value != rightline.value:
					values[i] = (leftline, rightline)


		if len(values) > 0:
			return (attr, values)
	else:
		if attr.type == 4:
			if (leftvalue is None) or (rightvalue is None):
				return (attr, leftvalue, rightvalue)
			elif leftvalue.choice != rightvalue.choice:
				return (attr, leftvalue, rightvalue)
		elif (attr.type == 1) or (attr.type == 2) or (attr.type == 3):
			if (leftvalue is None) or (rightvalue is None):
				return (attr, leftvalue, rightvalue)
			elif leftvalue.value != rightvalue.value:
				return (attr, leftvalue, rightvalue)
		

