from mcv.env import MCV_BASE_URL

def mcv(path: str) -> str:
    return MCV_BASE_URL + path