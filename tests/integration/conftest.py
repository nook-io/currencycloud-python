import os

import vcr
from vcr.record_mode import RecordMode

my_vcr = vcr.VCR(
    serializer="json",
    cassette_library_dir="tests/fixtures/vcr_cassettes",
    record_mode=RecordMode.NONE if os.environ.get("TRAVIS_GH3") else RecordMode.ONCE,
)
