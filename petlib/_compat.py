import cffi
import warnings


class OpenSSLVersion:
    V1_0 = "1_0"
    V1_1 = "1_1"


def _try_get_lib():
    try:
        from .bindings import _C
    except (ImportError, ValueError):
        pass

    ffi = cffi.FFI()
    ffi.cdef("long SSLeay(void);")
    ffi.cdef("unsigned long OpenSSL_version_num();")
    _C = ffi.dlopen("crypto")
    return _C


def get_openssl_version(warn=False):
    """Returns the OpenSSL version that is used for bindings."""

    lib = _try_get_lib()
    try:
        version = lib.OpenSSL_version_num() >> 20
    except AttributeError:
        version = lib.SSleay() >> 20

    print(hex(version))

    if version == 0x101:
        return OpenSSLVersion.V1_1
    elif version == 0x100:
        if warn:
            warnings.warn(
                    "Support for the system OpenSSL version (%d) is pending deprecation. "
                    "Please upgrade to OpenSSL v1.1" % version)
        return OpenSSLVersion.V1_0
    else:
        # If the version is not 1.0 or 1.1, assume its a later one, and optimistically
        # assume it doesn't horribly break the interface this time.
        if warn:
            warnings.warn(
                    "System OpenSSL version is not supported: %d. "
                    "Attempting to use in OpenSSL v1.1 mode." % version)
        return OpenSSLVersion.V1_1

