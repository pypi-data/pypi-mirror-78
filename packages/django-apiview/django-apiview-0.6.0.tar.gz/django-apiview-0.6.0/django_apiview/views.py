import time
import logging
import functools
import json

import bizerror
from fastutils import rsautils
from fastutils import strutils
from fastutils import funcutils
from fastutils import typingutils
from fastutils import cipherutils

from django.http import JsonResponse
from django.conf import settings

from .utils import SimpleJsonEncoder
from .utils import get_request_data
from .pack import SimpleJsonResultPacker
from .pack import SafeJsonResultPacker

logger = logging.getLogger(__name__)

simple_result_packer = SimpleJsonResultPacker()
safe_result_packer = SafeJsonResultPacker()

def setup_result_packer(packer):
    global simple_result_packer
    simple_result_packer = packer

class View(object):
    """Process class of apiview.
    """
    def __init__(self, request, defaults, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.data = {}
        self.data.update(defaults)
        self.data.update(get_request_data(self.request, self.kwargs))
        self.data["_django_apiview_view_instance"] = self

    def process(self, func):
        try:
            return func(_django_apiview_view_instance=self)
        except TypeError as error:
            if not str(error).endswith("got an unexpected keyword argument '_django_apiview_view_instance'"):
                raise error
            else:
                return funcutils.call_with_inject(func, self.data)

class Apiview(object):
    def __init__(self, packer, *preload_plugins):
        self.packer = packer
        self.preload_plugins = preload_plugins
    
    def __call__(self, func):
        """Turn the view function into apiview function. Must use as the first decorator.
        """
        def wrapper(request, **kwargs):
            target_func = func
            defaults = funcutils.get_default_values(func)
            view = View(request, defaults, **kwargs)
            package = {}
            try:
                for plugin in reversed(self.preload_plugins):
                    target_func = plugin(target_func)
                result = view.process(target_func)
                package = self.packer.pack_result(result)
            except Exception as error:
                logger.exception("apiview process failed: {}".format(str(error)))
                if not isinstance(error, bizerror.BizErrorBase):
                    error = bizerror.BizError(error)
                package = self.packer.pack_error(error)
            return JsonResponse(package, encoder=SimpleJsonEncoder, json_dumps_params={"ensure_ascii": False, "allow_nan": True, "sort_keys": True})
        wrapper.csrf_exempt = True
        return functools.wraps(func)(wrapper)

apiview = Apiview(simple_result_packer)


def requires(*parameter_names):
    """Throw bizerror.MissingParameter exception if required parameters not given.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            missing_names = []
            for name in parameter_names:
                if not name in view.data:
                    missing_names.append(name)
            if missing_names:
                raise bizerror.MissingParameter(missing_names)
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def choices(field, choices, annotation=None, allow_none=False):
    """Make sure field's value in choices.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            if callable(choices):
                params = get_inject_params(choices, view.data)
                values = choices(**params)
            else:
                values = choices
            value = view.data.get(field, None)
            if annotation:
                value = typingutils.smart_cast(annotation, value)
            if (allow_none and value is None) or (value in choices):
                return view.process(func)
            else:
                raise bizerror.BadParameter("field {0}'s value '{1}' is not in choices {2}.".format(field, value, values))
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def between(field, min, max, include_min=True, include_max=True, annotation=typingutils.Number, allow_none=False):
    """Make sure field's numeric value is in range of [min, max].
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            if callable(min):
                params = get_inject_params(min, view.data)
                min_value = min(**params)
            else:
                min_value = min
            if callable(max):
                params = get_inject_params(max, view.data)
                max_value = max(**params)
            else:
                max_value = max
            value = view.data.get(field, None)
            value = typingutils.smart_cast(typingutils.Number, value)
            if (allow_none and value is None) or ((include_min and min_value <= value or min_value < value) and (include_max and max_value >= value or max_value > value)):
                return view.process(func)
            else:
                raise bizerror.BadParameter("field {0}'s value '{1}' is not in range of {2}{3}, {4}{5}.".format(
                    field, value,
                    include_min and "[" or "(", 
                    min_value, max_value,
                    include_max and "]" or ")",
                    ))
        return functools.wraps(func)(wrapper)
    return wrapper_outer


def rsa_decrypt(field, private_key):
    """Do rsa-decrypt to the given field with private_key.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            if field in view.data:
                field_value = view.data[field]
                field_data = rsautils.smart_get_binary_data(field_value)
                plain_data = rsautils.decrypt(field_data, private_key)
                plain_text = plain_data.decode("utf-8")
                view.data[field] = plain_text
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer


def meta_variable(variable_name, meta_name):
    """Get variable from meta.
    """
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            value = view.request.META.get(meta_name, None)
            view.data[variable_name] = value
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer


def cache(key, expire=None, cache_name="default", get_from_cache=None, set_to_cache=True, disable_get_from_cache_header=getattr(settings, "DJANGO_APIVIEW_DISABLE_CACHE_HEADER_NAME", "HTTP_DISABLE_CACHE"), ignore_cache_errors=True):
    # Import here, so that we don't need django-redis by default.
    # Only if you use cache, then you need pip install django-redis
    from django_redis import get_redis_connection

    expire = expire or getattr(settings, "DJANGO_APIVIEW_DEFAULT_CACHE_EXPIRE", None)
    key_template = key
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            key = strutils.format_with_mapping(
                key_template,
                funcutils.chain(strutils.none_to_empty_string, strutils.strip_string),
                **view.data,
                )

            if get_from_cache == False:
                get_from_cache_final = False
            else:
                if view.request.META.get(disable_get_from_cache_header, "false") == "true":
                    get_from_cache_final = False
                else:
                    get_from_cache_final = True

            set_to_cache_final = set_to_cache
            use_cache = get_from_cache_final or set_to_cache_final

            cache = None
            if use_cache:
                try:
                    cache = get_redis_connection(cache_name)
                except Exception as error:
                    logger.error("get redis connection failed @cache, error_message={0}".format(str(error)))
                    if ignore_cache_errors:
                        cache = None
                    else:
                        raise
    
            if cache and get_from_cache:
                try:
                    result_text = cache.get(key)
                    if not result_text is None:
                        return json.loads(result_text)
                except Exception as error:
                    logger.error("query redis failed @cache, error_message={0}".format(str(error)))
                    if not ignore_cache_errors:
                        raise

            result = view.process(func)

            if cache and set_to_cache:
                try:
                    result_text = json.dumps(result, cls=SimpleJsonEncoder, allow_nan=True, sort_keys=True)
                    if expire:
                        cache.set(key, result_text,  keepttl=expire)
                    else:
                        cache.set(key, result_text)
                except Exception as error:
                    logger.error("write redis failed @cache, error_message={0}".format(str(error)))
                    if not ignore_cache_errors:
                        raise

            return result
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def load_client_rsa_publickey(get_client_rsa_publickey, client_id_fieldname="clientId", client_rsa_publickey_fieldname="CLIENT_RSA_PUBLICKEY"):
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            request = view.data["_request"]
            client_id = view.data.get(client_id_fieldname, None)
            if client_id:
                publickey = get_client_rsa_publickey(client_id)
                setattr(request, client_rsa_publickey_fieldname, publickey)
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def decode_encrypted_data(result_encoder=cipherutils.SafeBase64Encoder(), server_rsa_privatekey_filedname="RSA_PRIVATEKEY", encrypted_password_fieldname="encryptedPassword", encrypted_data_fieldname="encryptedData"):
    def wrapper_outer(func):
        def wrapper(_django_apiview_view_instance):
            view = _django_apiview_view_instance
            request = view.data["_request"]
            privatekey = getattr(settings, server_rsa_privatekey_filedname, None)
            encrypted_password = view.data.get(encrypted_password_fieldname, "")
            encrypted_data = view.data.get(encrypted_data_fieldname, "")
            if privatekey and encrypted_password and encrypted_data:
                password = rsautils.decrypt(encrypted_password, privatekey)
                cipher = cipherutils.AesCipher(password=password, result_encoder=result_encoder)
                data_text = cipher.decrypt(encrypted_data)
                data = json.loads(data_text)
                view.data.update(data)
            return view.process(func)
        return functools.wraps(func)(wrapper)
    return wrapper_outer

def safe_apiview(packer_class=SafeJsonResultPacker, **kwargs):
    return Apiview(
        funcutils.call_with_inject(packer_class, kwargs),
        funcutils.call_with_inject(load_client_rsa_publickey, kwargs),
        funcutils.call_with_inject(decode_encrypted_data, kwargs),
        )
