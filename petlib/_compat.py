import cffi
import warnings


OPENSSL_VERSION_1_0 = "1_0"
OPENSSL_VERSION_1_1 = "1_1"


def get_openssl_version_code(warn=False):
    """Returns system OpenSSL version code."""

    ffi = cffi.FFI()
    ffi.cdef("unsigned long OpenSSL_version_num();")
    lib = ffi.dlopen("crypto")
    version = lib.OpenSSL_version_num() >> 20

    if version == 0x101:
        return OPENSSL_VERSION_1_1
    elif version == 0x100:
        return OPENSSL_VERSION_1_0
    else:
        # If the version is not 1.0 or 1.1, assume its a later one, and optimistically
        # assume it doesn't horribly break the interface this time.
        if warn:
            warnings.warn(
                    "System OpenSSL version is not supported: %s. "
                    "Attempting to use in OpenSSL v1.1 mode." % ssl.OPENSSL_VERSION)
        return OPENSSL_VERSION_1_1

