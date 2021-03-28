from .couriers import CouriersView
from .courier import CourierView
from .orders import OrdersView
from .orders_assign import OrdersAssignView

HANDLERS = (CouriersView, CourierView, OrdersView, OrdersAssignView)
