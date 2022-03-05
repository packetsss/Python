import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "date_created")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class QuizQuery(graphene.ObjectType):
    """
    Frontend:

    {
        allQuestions {
            title
            quiz {
            id
            title
            category {
                name
            }
            dateCreated
            }
        }
        questionsById(id: $id) {
            title
            quiz {
            id
            title
            category {
                name
            }
            dateCreated
            }
        }
        allAnswers(id: $id) {
            question {
            title
            }
            answerText
        }
    }
    """

    all_questions = graphene.List(QuestionType)
    questions_by_id = graphene.Field(QuestionType, id=graphene.Int())

    # more than 1 answer for a question so use List
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_questions(root, info, id=None):
        return Question.objects.all()

    def resolve_questions_by_id(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        # query from foreign key question here and use filter to get more than 1 answer
        return Answer.objects.filter(question=id)


### CRUD ###
# create/update database
class CategoryMutation(graphene.Mutation):
    # input arguments for this mutation
    class Arguments:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)

    # class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id=None):
        # create a new category model
        if id is not None:
            category: Category = Category.objects.get(id=id)
            category.name = name
        else:
            category = Category(name=name)
        category.save()
        # make sure to return an instance of this mutation
        return CategoryMutation(category=category)


class DeleteCategory(graphene.Mutation):
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category: Category = Category.objects.get(id=id)
        category.delete()
        return cls(ok=True)


class QuizMutation(graphene.ObjectType):
    """
    Frontend:

    mutation CreateCategory {
      updateCategory(name: "Koofua") {
        category {
          name
        }
      }
    }
    """

    update_category = CategoryMutation.Field()
    delete_category = DeleteCategory.Field()


# delete from database


quiz_schema = graphene.Schema(query=QuizQuery, mutation=QuizMutation)
