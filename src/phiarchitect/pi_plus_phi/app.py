"""
run the main app
"""
from .pi_plus_phi import Pi_plus_phi


def run() -> None:
    reply = Pi_plus_phi().run()
    print(reply)
