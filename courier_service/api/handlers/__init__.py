from .couriers import CouriersView
from .courier import CourierView
from .orders import OrdersView
from .orders_assign import OrdersAssignView
from .order_complete import OrderCompleteView

HANDLERS = (CouriersView, CourierView, OrdersView, OrdersAssignView, OrderCompleteView)
