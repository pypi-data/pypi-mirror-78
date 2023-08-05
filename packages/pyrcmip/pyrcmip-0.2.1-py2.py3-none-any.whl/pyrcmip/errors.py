"""
Custom errors defined within pyrcmip
"""


class ProtocolConsistencyError(ValueError):
    """
    Inconsistency between input data and the RCMIP protocol
    """
