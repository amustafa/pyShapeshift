from .shapeshift_api import ShapeshiftAPI
from . import request_fns


api = ShapeshiftAPI(request_fns._sync_get_request,
                    request_fns._sync_post_request)
