import os

_data_dir = None
def data_dir():
    global _data_dir
    if _data_dir is None:
        p = os.path.join('woger', 'data')
        if os.path.exists(p):
            _data_dir = p

    return _data_dir

