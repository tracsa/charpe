from coralillo import Model, BoundedModel, fields


class Subscription(Model):
    channel = fields.TreeIndex()
    event   = fields.Text()
    user    = fields.ForeignIdRelation('lib.models.User', inverse='subscriptions')
    handler = fields.Text()
    params  = fields.Dict()


class User(Model):
    name      = fields.Text()
    last_name = fields.Text()
    email     = fields.Text(index=True, regex='^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$')
    is_active = fields.Bool(default=True)
    subscriptions = fields.SetRelation(Subscription, inverse='user')
    telegram_chat_id = fields.Text()
