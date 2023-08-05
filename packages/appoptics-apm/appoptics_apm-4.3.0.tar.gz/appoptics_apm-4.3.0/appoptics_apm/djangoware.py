"""AppOptics APM instrumentation for Django

 Copyright (C) 2016 by SolarWinds, LLC.
 All rights reserved.
"""
import functools
import threading
import time

from appoptics_apm import config, imports, util
from appoptics_apm.transaction_filter import UrlGetter

try:
    from django.utils.deprecation import MiddlewareMixin as AppOpticsApmMiddlewareBase
except ImportError:
    AppOpticsApmMiddlewareBase = object

# django middleware for passing values to appoptics_apm
__all__ = ("AppOpticsApmDjangoMiddleware", "install_appoptics_apm_middleware")

appoptics_apm_logger = util.logger


class DjangoUrlGetter(UrlGetter):
    """Reconstructs and stores the request URL"""
    def __init__(self, request):
        UrlGetter.__init__(self)
        self.request = request

    def set_url(self):
        self._url = self.request.build_absolute_uri()


class AppOpticsApmWSGIHandler(object):
    """ Wrapper WSGI Handler for Django's django.core.handlers.wsgi:WSGIHandler
    Can be used as a replacement for Django's WSGIHandler, e.g. with uWSGI.
    """
    def __init__(self):
        """ Import and instantiate django.core.handlers.WSGIHandler,
        now that the load_middleware wrapper below has been initialized. """
        from django.core.handlers.wsgi import WSGIHandler
        self._handler = WSGIHandler()

    def __call__(self, environ, start_response):
        return self._handler(environ, start_response)


# Middleware hooks listed here: http://docs.djangoproject.com/en/dev/ref/middleware/
class AppOpticsApmDjangoMiddleware(AppOpticsApmMiddlewareBase):
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        try:
            self.layer = settings.APPOPTICS_APM_BASE_LAYER
        except AttributeError:
            self.layer = 'django'
        super(AppOpticsApmDjangoMiddleware, self).__init__(*args, **kwargs)

    def _singleline(self, e):  # some logs like single-line errors better
        return str(e).replace('\n', ' ').replace('\r', ' ')

    def process_request(self, request):
        try:
            xtr_hdr = request.META.get("HTTP_X-Trace", request.META.get("HTTP_X_TRACE"))
            url = DjangoUrlGetter(request)
            ctx, start_evt = util.Context.start_trace(self.layer, xtr=xtr_hdr, url_getter=url)
            if ctx:
                # needs to be set regardless of sampling for metrics reporting
                setattr(util.Context.transaction_dict, 'url_tran', url.get_url())
                if ctx.is_sampled():
                    ctx.report(start_evt)
                    ctx.set_as_default()
            request.META.setdefault('APPOPTICS_APM_SPAN_START', str(int(time.time() * 1000000)))

        except Exception as e:
            appoptics_apm_logger.error("AppOptics APM middleware error: %s" % self._singleline(e))

    def process_view(self, request, view_func, view_args, view_kwargs):
        ctx = util.Context.get_default()
        if not ctx:
            return
        try:
            controller = getattr(view_func, '__module__', None)
            action = getattr(view_func, '__name__', None)

            if controller and action:
                request.META.setdefault('APPOPTICS_APM_SPAN_TRANSACTION', '{c}.{a}'.format(c=controller, a=action))

            if ctx.is_sampled():
                kvs = {
                    'Controller': controller,
                    'Action': action,
                }
                util.log('process_view', None, keys=kvs, store_backtrace=False)
        except Exception as e:
            appoptics_apm_logger.error("AppOptics APM middleware error: %s" % self._singleline(e))

    def process_response(self, request, response):
        """Process the response, record some information and send the end_trace out
        """
        ctx = util.Context.get_default()

        try:
            if ctx:
                # even if the request is not sampled, we need to gather this information to report metrics
                transaction_name = ctx.get_transaction_name()
                if not transaction_name:
                    transaction_name = request.META.pop('APPOPTICS_APM_SPAN_TRANSACTION', None)
                # exit event needs it. will be processed there
                domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META.get('HTTP_HOST', 'localhost'))

                setattr(util.Context.transaction_dict, 'domain', domain)
                setattr(util.Context.transaction_dict, 'transaction_name', transaction_name)
                setattr(util.Context.transaction_dict, 'start_time', request.META.pop('APPOPTICS_APM_SPAN_START', None))
                setattr(util.Context.transaction_dict, 'request_method', request.META.get('REQUEST_METHOD', 'GET'))
                setattr(util.Context.transaction_dict, 'status_code', response.status_code)

            x_trace = util.end_http_trace(self.layer)
            if x_trace:
                response['X-Trace'] = x_trace
                appoptics_apm_logger.debug("djangoware process_response x_trace: {x}".format(x=x_trace))
        except Exception as e:
            appoptics_apm_logger.error("AppOptics APM middleware error: %s" % self._singleline(e))

        return response

    def process_exception(self, request, exception):
        try:
            util.log_exception()
        except Exception as e:
            appoptics_apm_logger.error("AppOptics APM middleware error: %s" % self._singleline(e))


def middleware_hooks(module, objname):
    try:
        # wrap middleware callables we want to wrap
        cls = getattr(module, objname, None)
        appoptics_apm_logger.info('middleware_hooks module {m}'.format(m=module))
        if not cls:
            return
        for method in ['process_request',
                       'process_view',
                       'process_response',
                       'process_template_response',
                       'process_exception']:
            fn = getattr(cls, method, None)
            if not fn:
                continue
            profile_name = '%s.%s.%s' % (module.__name__, objname, method)
            setattr(cls, method, util.profile_function(profile_name)(fn))
    except Exception as e:
        appoptics_apm_logger.error("AppOptics APM error: %s" % str(e))


load_middleware_lock = threading.Lock()


def on_load_middleware():
    """ wrap Django middleware from a list """

    # protect middleware wrapping: only a single thread proceeds
    global load_middleware_lock  # lock gets overwritten as None after init
    if not load_middleware_lock:  # already initialized? abort
        return
    mwlock = load_middleware_lock
    mwlock.acquire()  # acquire global lock
    if not load_middleware_lock:  # check again
        mwlock.release()  # abort
        return
    load_middleware_lock = None  # mark global as "init done"

    try:
        # middleware hooks
        from django.conf import settings

        # settings.MIDDLEWARE_CLASSES is a tuple versions prior 1.9 and is list
        # in later versions. Versions since 1.10 use MIDDLEWARE instead of MIDDLEWARE_CLASSES.
        # however both attributes may exist in versions 1.10 and above.
        # The real type and value of settings.MIDDLEWARE and
        # settings.MIDDLEWARE_CLASSES are determined by the value in setting
        # file. Django.core.handler(1.11.16): load_middleware checks MIDDLEWARE first,
        # If it is none, it uses MIDDLEWARE_CLASSES, otherwise it uses
        # MIDDLEWARE. It doesn't check it's tuple or list, just iterate it.
        using_middleware_attr = True
        middleware = getattr(settings, 'MIDDLEWARE', None)
        if middleware is None:
            middleware = getattr(settings, 'MIDDLEWARE_CLASSES', None)
            using_middleware_attr = False

        for i in [] if middleware is None else middleware:
            if i.startswith('appoptics_apm'):
                continue
            dot = i.rfind('.')
            if dot < 0 or dot + 1 == len(i):
                continue
            objname = i[dot + 1:]
            imports.whenImported(i[:dot], functools.partial(middleware_hooks, objname=objname))
        # ORM
        if config['inst_enabled']['django_orm']:
            from appoptics_apm import inst_django_orm
            # The wrapper path BaseDatabaseWrapper has changed in Django 1.8 and onwards.
            try:
                import django.db.backends.base.base  # pylint: disable-msg=unused-import
                imports.whenImported('django.db.backends.base.base', inst_django_orm.wrap)
            except ImportError as e:
                appoptics_apm_logger.debug('AppOptics on_load_middleware: {e}, try loading dummy.base'.format(e=e))
                try:
                    import django.db.backends.dummy.base
                    imports.whenImported('django.db.backends.dummy.base', inst_django_orm.wrap)
                except ImportError as e:
                    appoptics_apm_logger.error('AppOptics error in on_load_middleware: {e}'.format(e=e))

        # templates
        if config['inst_enabled']['django_templates']:
            from appoptics_apm import inst_django_templates
            import django
            imports.whenImported('django.template.base', inst_django_templates.wrap)

        # load pluggable instrumentation
        from .loader import load_inst_modules
        load_inst_modules()
        apm_middleware = 'appoptics_apm.djangoware.AppOpticsApmDjangoMiddleware'
        if isinstance(middleware, list):
            middleware.insert(0, apm_middleware)
        elif isinstance(middleware, tuple):
            if using_middleware_attr:
                settings.MIDDLEWARE = (apm_middleware, ) + middleware
            else:
                settings.MIDDLEWARE_CLASSES = (apm_middleware, ) + middleware
        else:
            appoptics_apm_logger.error(
                "AppOptics APM error: settings middleware attribute should be either a tuple or a list,"
                "got {mw_type}".format(mw_type=str(type(middleware))))
    except Exception as e:
        appoptics_apm_logger.error('AppOptics APM error in on_load_middleware: {e}'.format(e=e))

    finally:  # release instrumentation lock
        mwlock.release()


def install_appoptics_apm_middleware(module):
    def base_handler_wrapper(func):
        @functools.wraps(func)  # XXX Not Python2.4-friendly
        def wrap_method(*f_args, **f_kwargs):
            on_load_middleware()
            return func(*f_args, **f_kwargs)

        return wrap_method

    try:
        cls = getattr(module, 'BaseHandler', None)
        try:
            if not cls or cls.APPOPTICS_APM_MIDDLEWARE_LOADER:
                return
        except AttributeError as e:
            cls.APPOPTICS_APM_MIDDLEWARE_LOADER = True
        fn = getattr(cls, 'load_middleware', None)
        setattr(cls, 'load_middleware', base_handler_wrapper(fn))
    except Exception as e:
        appoptics_apm_logger.error("AppOptics APM error: %s" % str(e))


if util.ready():
    try:
        imports.whenImported('django.core.handlers.base', install_appoptics_apm_middleware)
        # phone home
        util.report_layer_init(layer='django')
    except ImportError as e:
        # gracefully disable tracing if AppOptics APM lib not present
        appoptics_apm_logger.error("[AppOptics] Unable to instrument app and middleware: %s" % e)
