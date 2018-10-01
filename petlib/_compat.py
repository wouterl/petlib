import ssl
import warnings


def get_openssl_version_code(warn=False):
    """Returns system OpenSSL version code.

    :param warn: Whether to warn if the version is unknown.

    :return: One of ["1_0", "1_1"]
    """
    version_info = ssl.OPENSSL_VERSION_INFO
    major, minor = version_info[0], version_info[1]
    if major == 1 and minor == 1:
        return "1_1"
    elif major == 1 and minor == 0:
        return "1_0"
    else:
        # If the version is not 1.0 or 1.1, assume its a later one, and optimistically
        # assume it doesn't horribly break the interface this time.
        if warn:
            warnings.warn(
                    "System OpenSSL version is not supported: %s. "
                    "Attempting to use in OpenSSL v1.1 mode." % ssl.OPENSSL_VERSION)
        return "1_1"

