import graphene
from firebase_.firebase_db import list_files
"""
Things required for email request
attachments: images, pdf, zip files
template: html only
about: text
requested_by:
to_email:
"""

# Object Types/Custom Data type


class Email(graphene.ObjectType):
    attachments = graphene.List(graphene.String)
    template = graphene.NonNull(graphene.String)
    about = graphene.NonNull(graphene.String)
    requested_by = graphene.NonNull(graphene.String)
    to_email = graphene.List(graphene.NonNull(graphene.String))


class theFiles(graphene.ObjectType):
    files = graphene.List(graphene.String)


class Query(graphene.ObjectType):
    file_list = graphene.Field(theFiles)

    async def resolve_file_list(self, info):
        result = await list_files()
        print(result)
        return theFiles(result)


# Mutations
class TestEmail(graphene.Mutation):
    class Arguments:
        template = graphene.String()
        about = graphene.String()

    flag = graphene.Boolean()
    crap = graphene.String()

    def mutate(self, info, template, about):
        flag = True
        return TestEmail(flag=flag)


# schema
class AllMutations(graphene.ObjectType):
    test_email = TestEmail.Field()


schema = graphene.Schema(query=Query, mutation=AllMutations)
