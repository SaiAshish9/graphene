import graphene
import json
from datetime import datetime
import uuid


class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id=graphene.ID(default_value=str(uuid.uuid4()))
    username=graphene.String()
    created_at=graphene.DateTime(default_value=datetime.now())
    avatar_url=graphene.String()

    def resolve_avatar_url(self,info):
        return 'https://cloudinary.com/{}/{}'.format(self.username,self.id)


class Query(graphene.ObjectType):
    users=graphene.List(User,limit=graphene.Int())
    hello=graphene.String()
    is_admin=graphene.Boolean()

    def resolve_hello(self,info):
        return "world"

    def resolve_is_admin(self,info):
        return True
    
    def resolve_users(self,info,limit):
        return [
            User(id="1",username="Sai",created_at=datetime.now()),
            User(id="2",username="Ashish",created_at=datetime.now())
            
            ][:limit]


class CreateUser(graphene.Mutation):

    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self,info,username):
        user= User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):

    post=graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self,info,title,content):
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated')
        post=Post(title=title,content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

# schema=graphene.Schema(query=Query)
schema=graphene.Schema(query=Query,mutation=Mutation)
# ,auto_camelcase=False
# result = schema.execute(
#     '''
#     {
#         hello
#     }
#     '''
# )

#snakecase
# result=schema.execute(
# '''
# {
#    isAdmin    
# }
# '''    
# )

#camelcase
# result=schema.execute(
# '''
# {
#    is_admin    
# }
# '''    
# )

# result=schema.execute(
#     '''
#     {
#         users(limit:1) {
#             created_at
#             username
#         }
#     }
#     '''
# )

result=schema.execute(
    '''
    mutation($username:String) {
        createUser(username:$username) {
            user {
                id
                username
                createdAt
            }
        }
    }
    ''',
    variable_values={
        'username':'Sai'
    }

)

# !
result=schema.execute(
    '''
    query getQuery($limit:Int) {
        users(limit:$limit) {
                id
                username
                createdAt
        }
    }
    ''',
    variable_values={
        'limit':1
    }

)


result=schema.execute(
    '''
mutation{
    createPost(title:"hello",content:"world"){
        post{
            title
            content
        }
    }
}
    ''',
    context={'is_anonymous':True}

)

result=schema.execute(
    '''
    {
    users(limit:3) {
        avatarUrl
    }
    }
    '''
)


print(result.data.items())
# print(result.data['hello'])
print(json.dumps(dict(result.data.items())))
print(json.dumps(dict(result.data.items()),indent=2))

