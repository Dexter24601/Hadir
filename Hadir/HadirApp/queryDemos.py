from .models import User, Class

# ***(1)Returns all users from User table
users = User.objects.all()

# (2)Returns first User in table
firstUser = User.objects.first()

# (3)Returns last User in table
lastUser = User.objects.last()

# (4)Returns single User by name
userByName = User.objects.get(name='Peter Piper')

# ***(5)Returns single User by id
userById = User.objects.get(id=4)

# ***(6)Returns all orders related to User (firstUser variable set above)
firstUser.order_set.all()

# (7)***Returns orders User name: (Query parent model values)
order = Class.objects.first()
parentName = order.user.name

# (8)***Returns products from products table with value of "Out Door" in category attribut
products = Product.objects.filter(category="Out Door")

# (9)***Order/Sort Objects by id
leastToGreatest = Product.objects.all().order_by('id')
greatestToLeast = Product.objects.all().order_by('-id')

# (10) Returns all products with tag of “Sports”: (Query Many to Many Fields)
productFiltered = Product.object.filter(tags__name="Sports")


# parent = ParentModel.objects.first()
# #Returns all child models related to parent
# parent.childmodel_set.a11()
#
