import sys
from json import dumps
from textwrap import fill

from jwcrypto.jwk import JWK

from .lib import *

# issuer
ISSUER = "https://example.com/issuer"


# Define the claims
FULL_USER_CLAIMS = {
    "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
    "given_name": "John",
    "family_name": "Doe",
    "email": "johndoe@example.com",
    "phone_number": "+1-202-555-0101",
    "address": {
        "street_address": "123 Main St",
        "locality": "Anytown",
        "region": "Anystate",
        "country": "US",
    },
    "birthdate": "1940-01-01",
}

DISCLOSED_CLAIMS = {"given_name": None, "family_name": None, "address": None}


NONCE = generate_salt()

#######################################################################

print("# Creating the SD-JWT")


print(f"User claims:\n{dumps(FULL_USER_CLAIMS, indent=4)}")


sd_jwt_payload, serialized_sd_jwt, svc_payload, serialized_svc = create_sd_jwt_and_svc(
    FULL_USER_CLAIMS, ISSUER, ISSUER_KEY, HOLDER_KEY
)

print("Payload of the SD-JWT:\n" + dumps(sd_jwt_payload, indent=4) + "\n\n")

print("The serialized SD-JWT:\n" + serialized_sd_jwt + "\n\n")

print("Payload of the SD-JWT SVC:\n" + dumps(svc_payload, indent=4) + "\n\n")

print("The serialized SD-JWT SVC:\n" + serialized_svc + "\n\n")

combined_sd_jwt_svc = serialized_sd_jwt + "." + serialized_svc

#######################################################################

print("# Creating the SD-JWT-Release")


sd_jwt_release_payload, serialized_sd_jwt_release = create_release_jwt(
    NONCE, "https://example.com/verifier", DISCLOSED_CLAIMS, serialized_svc, HOLDER_KEY
)

print(
    "Payload of the SD-JWT-Release:\n"
    + dumps(sd_jwt_release_payload, indent=4)
    + "\n\n"
)


print("The serialized SD-JWT-Release:\n" + serialized_sd_jwt_release + "\n\n")

#######################################################################

print("# Creating the Combined Presentation")
# Combine both documents!
combined_sd_jwt_sd_jwt_release = serialized_sd_jwt + "." + serialized_sd_jwt_release

print("Combined Presentation:\n" + combined_sd_jwt_sd_jwt_release + "\n\n")

#######################################################################

print("# Verification")

# input: combined_sd_jwt_sd_jwt_release, holder_key, issuer_key

vc = verify(
    combined_sd_jwt_sd_jwt_release,
    ISSUER_PUBLIC_KEY,
    ISSUER,
    HOLDER_KEY,
    "https://example.com/verifier",
    NONCE,
)

print("Verified claims: " + dumps(vc, indent=4))

#######################################################################
# Replace the examples in the markdown file
#######################################################################


EXAMPLE_INDENT = 2
EXAMPLE_MAX_WIDTH = 70

if "--replace" in sys.argv:
    print("Replacing the placeholders in the main.md file")
    replacements = {
        "example-simple-sd-jwt-claims": dumps(FULL_USER_CLAIMS, indent=EXAMPLE_INDENT),
        "example-simple-sd-jwt-payload": dumps(sd_jwt_payload, indent=EXAMPLE_INDENT),
        "example-simple-sd-jwt-encoded": fill(
            serialized_sd_jwt, width=EXAMPLE_MAX_WIDTH, break_on_hyphens=False
        ),
        "example-simple-combined-sd-jwt-svc": fill(
            combined_sd_jwt_svc, width=EXAMPLE_MAX_WIDTH, break_on_hyphens=False
        ),
        "example-simple-svc-payload": dumps(svc_payload, indent=EXAMPLE_INDENT),
        "example-simple-combined-sd-jwt-sd-jwt-release": fill(
            combined_sd_jwt_sd_jwt_release,
            width=EXAMPLE_MAX_WIDTH,
            break_on_hyphens=False,
        ),
        "example-simple-release-payload": dumps(
            sd_jwt_release_payload, indent=EXAMPLE_INDENT
        ),
        "example-simple-release-encoded": fill(
            serialized_sd_jwt_release, width=EXAMPLE_MAX_WIDTH, break_on_hyphens=False
        ),
    }
    replace_all_in_main(replacements)
