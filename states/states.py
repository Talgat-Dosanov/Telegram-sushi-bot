from aiogram.dispatcher.filters.state import StatesGroup, State


class NewItem(StatesGroup):
    Order = State()
    EnterQuality = State()
    Approval = State()
    Delivery = State()
    PhoneNumber = State()

class AdminPanel(StatesGroup):
    Name = State()
    Category = State()
    Subcategory = State()
    Price = State()
    Description = State()
    Weight = State()
    Photo = State()
    Confirm = State()

class DeleteItem(StatesGroup):
    Item = State()

class Mailing(StatesGroup):
    Text = State()
    Photo = State()
    Confirm = State()

class ChangeItem(StatesGroup):
    ItemName = State()
    Changes = State()
    Price = State()
    Weight = State()
    Description = State()
    Photo = State()
    ConfirmChanges = State()