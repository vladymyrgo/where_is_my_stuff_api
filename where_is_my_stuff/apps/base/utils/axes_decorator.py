import logging

import axes.decorators as decorators
from axes.decorators import get_ip, check_request

from axes.models import AccessLog


VERBOSE = decorators.VERBOSE
USERNAME_FORM_FIELD = decorators.USERNAME_FORM_FIELD
LOGGER = decorators.LOGGER

log = logging.getLogger(LOGGER)


def watch_login(func):
    """
    Decorator from axes.decorators with additional logic for DRF login view.
    """

    # Don't decorate multiple times
    if func.__name__ == 'decorated_login':  # pragma: no cover
        return func

    def decorated_login(request, *args, **kwargs):
        # share some useful information
        if func.__name__ != 'decorated_login' and VERBOSE:  # pragma: no cover
            log.info('AXES: Calling decorated function: %s' % func.__name__)
            if args:
                log.info('args: %s' % str(args))
            if kwargs:
                log.info('kwargs: %s' % kwargs)

        # call the login function
        response = func(request, *args, **kwargs)

        if func.__name__ == 'decorated_login':  # pragma: no cover
            return response

        if request.method == 'POST':
            # see if the login was successful
            login_unsuccessful = (
                response and
                not response.has_header('location') and
                response.status_code != 302
            )

            user_agent = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
            http_accept = request.META.get('HTTP_ACCEPT', '<unknown>')[:1025]
            path_info = request.META.get('PATH_INFO', '<unknown>')[:255]
            AccessLog.objects.create(
                user_agent=user_agent,
                ip_address=get_ip(request),
                username=request.POST.get(USERNAME_FORM_FIELD, None),
                http_accept=http_accept,
                path_info=path_info,
                trusted=not login_unsuccessful,
            )
            if check_request(request, login_unsuccessful):
                return response
            else:
                response.data = {"error_type": "LoginAttemptsExceededError"}
                response.content = response.rendered_content
                return response

        return response

    return decorated_login
