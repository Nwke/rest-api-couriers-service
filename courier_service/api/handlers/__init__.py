from .couriers import CouriersView
from .courier import CourierView
from .order import OrderView
from .order_assign import OrderAssignView

HANDLERS = (CouriersView, CourierView, OrderView, OrderAssignView)
