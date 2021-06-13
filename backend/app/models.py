from mongoengine import Document, fields


class Region(Document):
    vkId = fields.IntField(required=True)
    title = fields.StringField(required=True)


class City(Document):
    vkId = fields.IntField(required=True)
    title = fields.StringField(trim=True, required=True)
    area = fields.StringField(trim=True, required=False)
    region = fields.ReferenceField(Region, required=True)


class Institute(Document):
    code = fields.IntField(required=True)
    title = fields.StringField(required=True)


class VkUser(Document):
    vkId = fields.IntField(required=True)
    firstName = fields.StringField(trim=True, required=True)
    lastName = fields.StringField(trim=True, required=True)
    bdate = fields.StringField(trim=True)
    groups = fields.ListField(fields.StringField(trim=True))
    city = fields.ReferenceField(City, required=True)
    totalGroups = fields.IntField()
    allowedGroups = fields.IntField()
    successPercentage = fields.IntField()
    institute = fields.ReferenceField(Institute, required=True)
    # institute = fields.ReferenceField(required=True)  # qweqeqew
