# This is replaced during release process.
__version_suffix__ = '119'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.18.8"
KUBECTL_SHA512 = {
    "linux": "041dd919f7bf530e6fb6881bc475dbd34cec340eae62193cba1174a0fa0b9d30435b74b0a130db4cdabf35dc59c1bf6bc255e4f91c8ec9a839fb541735e3861e",
    "darwin": "2c700d683bc732cd4e353d31528bb6996cbf0f6d7e5dc93fbf45b4d457d5598cfd92762aa2106af8300d3fa39596c6710a3ea5248424bc28eddd53354bd9b0a6",
}

STERN_VERSION = "1.11.0"
STERN_SHA256 = {
    "linux": "e0b39dc26f3a0c7596b2408e4fb8da533352b76aaffdc18c7ad28c833c9eb7db",
    "darwin": "7aea3b6691d47b3fb844dfc402905790665747c1e6c02c5cabdd41994533d7e9",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
