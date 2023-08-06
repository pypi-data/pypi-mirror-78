import graphene

class BaseObjectType(graphene.ObjectType):
    @classmethod
    async def resolve_id(cls, root, info):
        return root.get('_id')
