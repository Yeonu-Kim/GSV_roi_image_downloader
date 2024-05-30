# If there is panoID already, return False
def isAlreadyDownloaded(panoID: str, panoIDList: list):
    return panoID in panoIDList