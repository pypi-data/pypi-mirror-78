/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

#include <errno.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "error/s2n_errno.h"

#include <s2n.h>
#include "utils/s2n_map.h"
#include "utils/s2n_safety.h"

#if S2N_HAVE_EXECINFO
#   include <execinfo.h>
#endif

__thread int s2n_errno;
__thread const char *s2n_debug_str;

static const char *no_such_language = "Language is not supported for error translation";
static const char *no_such_error = "Internal s2n error";

/*
 * Define error entries with descriptions in this macro once
 * to generate code in next 2 following functions.
 */
#define ERR_ENTRIES(ERR_ENTRY) \
    ERR_ENTRY(S2N_ERR_OK, "no error") \
    ERR_ENTRY(S2N_ERR_IO, "underlying I/O operation failed, check system errno") \
    ERR_ENTRY(S2N_ERR_CLOSED, "connection is closed") \
    ERR_ENTRY(S2N_ERR_BLOCKED, "underlying I/O operation would block") \
    ERR_ENTRY(S2N_ERR_ALERT, "TLS alert received") \
    ERR_ENTRY(S2N_ERR_ENCRYPT, "error encrypting data") \
    ERR_ENTRY(S2N_ERR_DECRYPT, "error decrypting data") \
    ERR_ENTRY(S2N_ERR_BAD_MESSAGE, "Bad message encountered") \
    ERR_ENTRY(S2N_ERR_KEY_INIT, "error initializing encryption key") \
    ERR_ENTRY(S2N_ERR_DH_SERIALIZING, "error serializing Diffie-Hellman parameters") \
    ERR_ENTRY(S2N_ERR_DH_SHARED_SECRET, "error computing Diffie-Hellman shared secret") \
    ERR_ENTRY(S2N_ERR_DH_WRITING_PUBLIC_KEY, "error writing Diffie-Hellman public key") \
    ERR_ENTRY(S2N_ERR_DH_FAILED_SIGNING, "error signing Diffie-Hellman values") \
    ERR_ENTRY(S2N_ERR_DH_COPYING_PARAMETERS, "error copying Diffie-Hellman parameters") \
    ERR_ENTRY(S2N_ERR_DH_GENERATING_PARAMETERS, "error generating Diffie-Hellman parameters") \
    ERR_ENTRY(S2N_ERR_CIPHER_NOT_SUPPORTED, "Cipher is not supported") \
    ERR_ENTRY(S2N_ERR_NO_APPLICATION_PROTOCOL, "No supported application protocol to negotiate") \
    ERR_ENTRY(S2N_ERR_FALLBACK_DETECTED, "TLS fallback detected") \
    ERR_ENTRY(S2N_ERR_HASH_DIGEST_FAILED, "failed to create hash digest") \
    ERR_ENTRY(S2N_ERR_HASH_INIT_FAILED, "error initializing hash") \
    ERR_ENTRY(S2N_ERR_HASH_UPDATE_FAILED, "error updating hash") \
    ERR_ENTRY(S2N_ERR_HASH_COPY_FAILED, "error copying hash") \
    ERR_ENTRY(S2N_ERR_HASH_WIPE_FAILED, "error wiping hash") \
    ERR_ENTRY(S2N_ERR_HASH_NOT_READY, "hash not in a valid state for the attempted operation") \
    ERR_ENTRY(S2N_ERR_ALLOW_MD5_FOR_FIPS_FAILED, "error allowing MD5 to be used when in FIPS mode") \
    ERR_ENTRY(S2N_ERR_DECODE_CERTIFICATE, "error decoding certificate") \
    ERR_ENTRY(S2N_ERR_DECODE_PRIVATE_KEY, "error decoding private key") \
    ERR_ENTRY(S2N_ERR_INVALID_SIGNATURE_ALGORITHM, "Invalid signature algorithm") \
    ERR_ENTRY(S2N_ERR_INVALID_SIGNATURE_SCHEME, "Invalid signature scheme") \
    ERR_ENTRY(S2N_ERR_EMPTY_SIGNATURE_SCHEME, "Empty signature scheme") \
    ERR_ENTRY(S2N_ERR_CBC_VERIFY, "Failed CBC verification") \
    ERR_ENTRY(S2N_ERR_DH_COPYING_PUBLIC_KEY, "error copying Diffie-Hellman public key") \
    ERR_ENTRY(S2N_ERR_SIGN, "error signing data") \
    ERR_ENTRY(S2N_ERR_VERIFY_SIGNATURE, "error verifying signature") \
    ERR_ENTRY(S2N_ERR_ECDHE_GEN_KEY, "Failed to generate an ECDHE key") \
    ERR_ENTRY(S2N_ERR_ECDHE_SHARED_SECRET, "Error computing ECDHE shared secret") \
    ERR_ENTRY(S2N_ERR_ECDHE_UNSUPPORTED_CURVE, "Unsupported EC curve was presented during an ECDHE handshake") \
    ERR_ENTRY(S2N_ERR_ECDSA_UNSUPPORTED_CURVE, "Unsupported EC curve was presented during an ECDSA SignatureScheme handshake") \
    ERR_ENTRY(S2N_ERR_ECDHE_SERIALIZING, "Error serializing ECDHE public") \
    ERR_ENTRY(S2N_ERR_KEM_UNSUPPORTED_PARAMS, "Unsupported KEM params was presented during a handshake that uses a KEM") \
    ERR_ENTRY(S2N_ERR_SHUTDOWN_RECORD_TYPE, "Non alert record received during s2n_shutdown()") \
    ERR_ENTRY(S2N_ERR_SHUTDOWN_CLOSED, "Peer closed before sending their close_notify") \
    ERR_ENTRY(S2N_ERR_NON_EMPTY_RENEGOTIATION_INFO, "renegotiation_info should be empty") \
    ERR_ENTRY(S2N_ERR_RECORD_LIMIT, "TLS record limit reached") \
    ERR_ENTRY(S2N_ERR_CERT_UNTRUSTED, "Certificate is untrusted") \
    ERR_ENTRY(S2N_ERR_CERT_TYPE_UNSUPPORTED, "Certificate Type is unsupported") \
    ERR_ENTRY(S2N_ERR_INVALID_MAX_FRAG_LEN, "invalid Maximum Fragmentation Length encountered") \
    ERR_ENTRY(S2N_ERR_MAX_FRAG_LEN_MISMATCH, "Negotiated Maximum Fragmentation Length from server does not match the requested length by client") \
    ERR_ENTRY(S2N_ERR_PROTOCOL_VERSION_UNSUPPORTED, "TLS protocol version is not supported by selected cipher suite") \
    ERR_ENTRY(S2N_ERR_BAD_KEY_SHARE, "Bad key share received") \
    ERR_ENTRY(S2N_ERR_CANCELLED, "handshake was cancelled") \
    ERR_ENTRY(S2N_ERR_PROTOCOL_DOWNGRADE_DETECTED, "Protocol downgrade detected by client") \
    ERR_ENTRY(S2N_ERR_MADVISE, "error calling madvise") \
    ERR_ENTRY(S2N_ERR_ALLOC, "error allocating memory") \
    ERR_ENTRY(S2N_ERR_MLOCK, "error calling mlock (Did you run prlimit?)") \
    ERR_ENTRY(S2N_ERR_MUNLOCK, "error calling munlock") \
    ERR_ENTRY(S2N_ERR_FSTAT, "error calling fstat") \
    ERR_ENTRY(S2N_ERR_OPEN, "error calling open") \
    ERR_ENTRY(S2N_ERR_MMAP, "error calling mmap") \
    ERR_ENTRY(S2N_ERR_ATEXIT, "error calling atexit") \
    ERR_ENTRY(S2N_ERR_NOMEM, "no memory") \
    ERR_ENTRY(S2N_ERR_NULL, "NULL pointer encountered") \
    ERR_ENTRY(S2N_ERR_SAFETY, "a safety check failed") \
    ERR_ENTRY(S2N_ERR_NOT_INITIALIZED, "s2n not initialized") \
    ERR_ENTRY(S2N_ERR_RANDOM_UNINITIALIZED, "s2n entropy not initialized") \
    ERR_ENTRY(S2N_ERR_OPEN_RANDOM, "error opening urandom") \
    ERR_ENTRY(S2N_ERR_RESIZE_STATIC_STUFFER, "cannot resize a static stuffer") \
    ERR_ENTRY(S2N_ERR_RESIZE_TAINTED_STUFFER, "cannot resize a tainted stuffer") \
    ERR_ENTRY(S2N_ERR_STUFFER_OUT_OF_DATA, "stuffer is out of data") \
    ERR_ENTRY(S2N_ERR_STUFFER_IS_FULL, "stuffer is full") \
    ERR_ENTRY(S2N_ERR_STUFFER_NOT_FOUND, "stuffer expected bytes were not found") \
    ERR_ENTRY(S2N_ERR_STUFFER_HAS_UNPROCESSED_DATA, "stuffer has unprocessed data") \
    ERR_ENTRY(S2N_ERR_HASH_INVALID_ALGORITHM, "invalid hash algorithm") \
    ERR_ENTRY(S2N_ERR_PRF_INVALID_ALGORITHM, "invalid prf hash algorithm") \
    ERR_ENTRY(S2N_ERR_PRF_INVALID_SEED, "invalid prf seeds provided") \
    ERR_ENTRY(S2N_ERR_P_HASH_INVALID_ALGORITHM, "invalid p_hash algorithm") \
    ERR_ENTRY(S2N_ERR_P_HASH_INIT_FAILED, "error initializing p_hash") \
    ERR_ENTRY(S2N_ERR_P_HASH_UPDATE_FAILED, "error updating p_hash") \
    ERR_ENTRY(S2N_ERR_P_HASH_FINAL_FAILED, "error creating p_hash digest") \
    ERR_ENTRY(S2N_ERR_P_HASH_WIPE_FAILED, "error wiping p_hash") \
    ERR_ENTRY(S2N_ERR_HMAC_INVALID_ALGORITHM, "invalid HMAC algorithm") \
    ERR_ENTRY(S2N_ERR_HKDF_OUTPUT_SIZE, "invalid HKDF output size") \
    ERR_ENTRY(S2N_ERR_ALERT_PRESENT, "TLS alert is already pending") \
    ERR_ENTRY(S2N_ERR_HANDSHAKE_STATE, "Invalid handshake state encountered") \
    ERR_ENTRY(S2N_ERR_SHUTDOWN_PAUSED, "s2n_shutdown() called while paused") \
    ERR_ENTRY(S2N_ERR_SIZE_MISMATCH, "size mismatch") \
    ERR_ENTRY(S2N_ERR_DRBG, "Error using Deterministic Random Bit Generator") \
    ERR_ENTRY(S2N_ERR_DRBG_REQUEST_SIZE, "Request for too much entropy") \
    ERR_ENTRY(S2N_ERR_KEY_CHECK, "Invalid key") \
    ERR_ENTRY(S2N_ERR_CIPHER_TYPE, "Unknown cipher type used") \
    ERR_ENTRY(S2N_ERR_MAP_DUPLICATE, "Duplicate map key inserted") \
    ERR_ENTRY(S2N_ERR_MAP_IMMUTABLE, "Attempt to update an immutable map") \
    ERR_ENTRY(S2N_ERR_MAP_MUTABLE, "Attempt to lookup a mutable map") \
    ERR_ENTRY(S2N_ERR_MAP_INVALID_MAP_SIZE, "Attempt to create a map with 0 capacity") \
    ERR_ENTRY(S2N_ERR_INITIAL_HMAC, "error calling EVP_CIPHER_CTX_ctrl for composite cbc cipher") \
    ERR_ENTRY(S2N_ERR_INVALID_NONCE_TYPE, "Invalid AEAD nonce type") \
    ERR_ENTRY(S2N_ERR_UNIMPLEMENTED, "Unimplemented feature") \
    ERR_ENTRY(S2N_ERR_READ, "error calling read") \
    ERR_ENTRY(S2N_ERR_WRITE, "error calling write") \
    ERR_ENTRY(S2N_ERR_BAD_FD, "Invalid file descriptor") \
    ERR_ENTRY(S2N_ERR_RDRAND_FAILED, "Error executing rdrand instruction") \
    ERR_ENTRY(S2N_ERR_FAILED_CACHE_RETRIEVAL, "Failed cache retrieval") \
    ERR_ENTRY(S2N_ERR_X509_TRUST_STORE, "Error initializing trust store") \
    ERR_ENTRY(S2N_ERR_UNKNOWN_PROTOCOL_VERSION, "Error determining client protocol version") \
    ERR_ENTRY(S2N_ERR_NULL_CN_NAME, "Error parsing CN names") \
    ERR_ENTRY(S2N_ERR_NULL_SANS, "Error parsing SANS") \
    ERR_ENTRY(S2N_ERR_CLIENT_HELLO_VERSION, "Could not get client hello version") \
    ERR_ENTRY(S2N_ERR_CLIENT_PROTOCOL_VERSION, "Could not get client protocol version") \
    ERR_ENTRY(S2N_ERR_SERVER_PROTOCOL_VERSION, "Could not get server protocol version") \
    ERR_ENTRY(S2N_ERR_ACTUAL_PROTOCOL_VERSION, "Could not get actual protocol version") \
    ERR_ENTRY(S2N_ERR_POLLING_FROM_SOCKET, "Error polling from socket") \
    ERR_ENTRY(S2N_ERR_RECV_STUFFER_FROM_CONN, "Error receiving stuffer from connection") \
    ERR_ENTRY(S2N_ERR_SEND_STUFFER_TO_CONN, "Error sending stuffer to connection") \
    ERR_ENTRY(S2N_ERR_PRECONDITION_VIOLATION, "Precondition violation") \
    ERR_ENTRY(S2N_ERR_INTEGER_OVERFLOW, "Integer overflow violation") \
    ERR_ENTRY(S2N_ERR_ARRAY_INDEX_OOB, "Array index out of bounds") \
    ERR_ENTRY(S2N_ERR_FREE_STATIC_BLOB, "Cannot free a static blob") \
    ERR_ENTRY(S2N_ERR_RESIZE_STATIC_BLOB, "Cannot resize a static blob") \
    ERR_ENTRY(S2N_ERR_NO_AVAILABLE_BORINGSSL_API, "BoringSSL does not support this API") \
    ERR_ENTRY(S2N_ERR_NO_ALERT, "No Alert present") \
    ERR_ENTRY(S2N_ERR_CLIENT_MODE, "operation not allowed in client mode") \
    ERR_ENTRY(S2N_ERR_CLIENT_MODE_DISABLED, "client connections not allowed") \
    ERR_ENTRY(S2N_ERR_TOO_MANY_CERTIFICATES, "only 1 certificate is supported in client mode") \
    ERR_ENTRY(S2N_ERR_TOO_MANY_SIGNATURE_SCHEMES, "Max supported length of SignatureAlgorithms/SignatureSchemes list is 32") \
    ERR_ENTRY(S2N_ERR_CLIENT_AUTH_NOT_SUPPORTED_IN_FIPS_MODE, "Client Auth is not supported when in FIPS mode") \
    ERR_ENTRY(S2N_ERR_INVALID_BASE64, "invalid base64 encountered") \
    ERR_ENTRY(S2N_ERR_INVALID_HEX, "invalid HEX encountered") \
    ERR_ENTRY(S2N_ERR_INVALID_PEM, "invalid PEM encountered") \
    ERR_ENTRY(S2N_ERR_DH_PARAMS_CREATE, "error creating Diffie-Hellman parameters") \
    ERR_ENTRY(S2N_ERR_DH_TOO_SMALL, "Diffie-Hellman parameters are too small") \
    ERR_ENTRY(S2N_ERR_DH_PARAMETER_CHECK, "Diffie-Hellman parameter check failed") \
    ERR_ENTRY(S2N_ERR_INVALID_PKCS3, "invalid PKCS3 encountered") \
    ERR_ENTRY(S2N_ERR_NO_CERTIFICATE_IN_PEM, "No certificate in PEM") \
    ERR_ENTRY(S2N_ERR_SERVER_NAME_TOO_LONG, "server name is too long") \
    ERR_ENTRY(S2N_ERR_NUM_DEFAULT_CERTIFICATES, "exceeded max default certificates or provided no default") \
    ERR_ENTRY(S2N_ERR_MULTIPLE_DEFAULT_CERTIFICATES_PER_AUTH_TYPE, "setting multiple default certificates per auth type is not allowed") \
    ERR_ENTRY(S2N_ERR_INVALID_CIPHER_PREFERENCES, "Invalid Cipher Preferences version") \
    ERR_ENTRY(S2N_ERR_APPLICATION_PROTOCOL_TOO_LONG, "Application protocol name is too long") \
    ERR_ENTRY(S2N_ERR_KEY_MISMATCH, "public and private key do not match") \
    ERR_ENTRY(S2N_ERR_SEND_SIZE, "Retried s2n_send() size is invalid") \
    ERR_ENTRY(S2N_ERR_CORK_SET_ON_UNMANAGED, "Attempt to set connection cork management on unmanaged IO") \
    ERR_ENTRY(S2N_ERR_UNRECOGNIZED_EXTENSION, "TLS extension not recognized") \
    ERR_ENTRY(S2N_ERR_INVALID_SCT_LIST, "SCT list is invalid") \
    ERR_ENTRY(S2N_ERR_INVALID_OCSP_RESPONSE, "OCSP response is invalid") \
    ERR_ENTRY(S2N_ERR_UPDATING_EXTENSION, "Updating extension data failed") \
    ERR_ENTRY(S2N_ERR_INVALID_SERIALIZED_SESSION_STATE, "Serialized session state is not in valid format") \
    ERR_ENTRY(S2N_ERR_SERIALIZED_SESSION_STATE_TOO_LONG, "Serialized session state is too long") \
    ERR_ENTRY(S2N_ERR_SESSION_ID_TOO_LONG, "Session id is too long") \
    ERR_ENTRY(S2N_ERR_CLIENT_AUTH_NOT_SUPPORTED_IN_SESSION_RESUMPTION_MODE, "Client Auth is not supported in session resumption mode") \
    ERR_ENTRY(S2N_ERR_INVALID_TICKET_KEY_LENGTH, "Session ticket key length cannot be zero") \
    ERR_ENTRY(S2N_ERR_INVALID_TICKET_KEY_NAME_OR_NAME_LENGTH, "Session ticket key name should be unique and the name length cannot be zero") \
    ERR_ENTRY(S2N_ERR_TICKET_KEY_NOT_UNIQUE, "Cannot add session ticket key because it was added before") \
    ERR_ENTRY(S2N_ERR_TICKET_KEY_LIMIT, "Limit reached for unexpired session ticket keys") \
    ERR_ENTRY(S2N_ERR_NO_TICKET_ENCRYPT_DECRYPT_KEY, "No key in encrypt-decrypt state is available to encrypt session ticket") \
    ERR_ENTRY(S2N_ERR_ENCRYPT_DECRYPT_KEY_SELECTION_FAILED, "Failed to select a key from keys in encrypt-decrypt state") \
    ERR_ENTRY(S2N_ERR_KEY_USED_IN_SESSION_TICKET_NOT_FOUND, "Key used in already assigned session ticket not found for decryption") \
    ERR_ENTRY(S2N_ERR_SENDING_NST, "Error in session ticket status encountered before sending NST") \
    ERR_ENTRY(S2N_ERR_INVALID_DYNAMIC_THRESHOLD, "invalid dynamic record threshold") \
    ERR_ENTRY(S2N_ERR_INVALID_ARGUMENT, "invalid argument provided into a function call") \
    ERR_ENTRY(S2N_ERR_NOT_IN_UNIT_TEST, "Illegal configuration, can only be used during unit tests") \
    ERR_ENTRY(S2N_ERR_UNSUPPORTED_CPU, "Unsupported CPU architecture") \
    ERR_ENTRY(S2N_ERR_SESSION_ID_TOO_SHORT, "Session id is too short") \
    ERR_ENTRY(S2N_ERR_CONNECTION_CACHING_DISALLOWED, "This connection is not allowed to be cached") \
    ERR_ENTRY(S2N_ERR_SESSION_TICKET_NOT_SUPPORTED, "Session ticket not supported for this connection") \
    ERR_ENTRY(S2N_ERR_OCSP_NOT_SUPPORTED, "OCSP stapling was requested, but is not supported") \
    ERR_ENTRY(S2N_ERR_INVALID_SIGNATURE_ALGORITHMS_PREFERENCES, "Invalid signature algorithms preferences version") \
    ERR_ENTRY(S2N_ERR_PQ_KEMS_DISALLOWED_IN_FIPS, "PQ KEMs are disallowed while in FIPS mode") \
    ERR_ENTRY(S2N_RSA_PSS_NOT_SUPPORTED, "RSA-PSS signing not supported by underlying libcrypto implementation") \
    ERR_ENTRY(S2N_ERR_MAX_INNER_PLAINTEXT_SIZE, "inner plaintext size exceeds limit") \
    ERR_ENTRY(S2N_ERR_INVALID_ECC_PREFERENCES, "Invalid ecc curves preferences version") \
    
#define ERR_STR_CASE(ERR, str) case ERR: return str;
#define ERR_NAME_CASE(ERR, str) case ERR: return #ERR;

const char *s2n_strerror(int error, const char *lang)
{
    if (lang == NULL) {
        lang = "EN";
    }

    if (strcasecmp(lang, "EN")) {
        return no_such_language;
    }

    s2n_error err = error;
    switch (err) {
        ERR_ENTRIES(ERR_STR_CASE)

        /* Skip block ends */
        case S2N_ERR_T_OK_END:
        case S2N_ERR_T_IO_END:
        case S2N_ERR_T_CLOSED_END:
        case S2N_ERR_T_BLOCKED_END:
        case S2N_ERR_T_ALERT_END:
        case S2N_ERR_T_PROTO_END:
        case S2N_ERR_T_INTERNAL_END:
        case S2N_ERR_T_USAGE_END:
            break;

        /* No default to make compiler fail on missing values */
    }

    return no_such_error;
}

const char *s2n_strerror_name(int error)
{
    s2n_error err = error;
    switch (err) {
        ERR_ENTRIES(ERR_NAME_CASE)

        /* Skip block ends */
        case S2N_ERR_T_OK_END:
        case S2N_ERR_T_IO_END:
        case S2N_ERR_T_CLOSED_END:
        case S2N_ERR_T_BLOCKED_END:
        case S2N_ERR_T_ALERT_END:
        case S2N_ERR_T_PROTO_END:
        case S2N_ERR_T_INTERNAL_END:
        case S2N_ERR_T_USAGE_END:
            break;

        /* No default to make compiler fail on missing values */
    }

    return no_such_error;
}

const char *s2n_strerror_debug(int error, const char *lang)
{
    if (lang == NULL) {
        lang = "EN";
    }

    if (strcasecmp(lang, "EN")) {
        return no_such_language;
    }

    /* No error, just return the no error string */
    if (error == S2N_ERR_OK) {
        return s2n_strerror(error, lang);
    }

    return s2n_debug_str;
}

int s2n_error_get_type(int error)
{
    return (error >> S2N_ERR_NUM_VALUE_BITS);
}


/* https://www.gnu.org/software/libc/manual/html_node/Backtraces.html */
static bool s_s2n_stack_traces_enabled = false;

bool s2n_stack_traces_enabled()
{
    return s_s2n_stack_traces_enabled;
}

int s2n_stack_traces_enabled_set(bool newval)
{
    s_s2n_stack_traces_enabled = newval;
    return S2N_SUCCESS;
}

#ifdef S2N_HAVE_EXECINFO

#define MAX_BACKTRACE_DEPTH 20
__thread struct s2n_stacktrace tl_stacktrace = {0};

int s2n_free_stacktrace(void)
{
    if (tl_stacktrace.trace != NULL) {
        free(tl_stacktrace.trace);
	struct s2n_stacktrace zero_stacktrace = {0};
	tl_stacktrace = zero_stacktrace;
    }
    return S2N_SUCCESS;
}

int s2n_calculate_stacktrace(void)
{
    if (!s_s2n_stack_traces_enabled) {
        return S2N_SUCCESS;
    }

    int old_errno = errno;
    GUARD(s2n_free_stacktrace());
    void *array[MAX_BACKTRACE_DEPTH];
    tl_stacktrace.trace_size = backtrace(array, MAX_BACKTRACE_DEPTH);
    tl_stacktrace.trace = backtrace_symbols(array, tl_stacktrace.trace_size);
    errno = old_errno;
    return S2N_SUCCESS;
}

int s2n_get_stacktrace(struct s2n_stacktrace *trace) {
    *trace = tl_stacktrace;
    return S2N_SUCCESS;
}

int s2n_print_stacktrace(FILE *fptr)
{
    if (!s_s2n_stack_traces_enabled) {
      fprintf(fptr, "%s\n%s\n",
	      "NOTE: Some details are omitted, run with S2N_PRINT_STACKTRACE=1 for a verbose backtrace.",
	      "See https://github.com/awslabs/s2n/blob/master/docs/USAGE-GUIDE.md");
        return S2N_SUCCESS;
    }

    fprintf(fptr, "\nStacktrace is:\n");
    for (int i = 0; i < tl_stacktrace.trace_size; ++i){
        fprintf(fptr, "%s\n",  tl_stacktrace.trace[i]);
    }
    return S2N_SUCCESS;
}

#else /* !S2N_HAVE_EXECINFO */
int s2n_free_stacktrace(void)
{
    S2N_ERROR(S2N_ERR_UNIMPLEMENTED);
}

int s2n_calculate_stacktrace(void)
{
    if (!s_s2n_stack_traces_enabled)
    {
        return S2N_SUCCESS;
    }

    S2N_ERROR(S2N_ERR_UNIMPLEMENTED);
}

int s2n_get_stacktrace(struct s2n_stacktrace *trace)
{
    S2N_ERROR(S2N_ERR_UNIMPLEMENTED);
}

int s2n_print_stacktrace(FILE *fptr)
{
    S2N_ERROR(S2N_ERR_UNIMPLEMENTED);
}
#endif /* S2N_HAVE_EXECINFO */
