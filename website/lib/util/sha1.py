import hashlib

def sha1_by_file(file):

    try:
        sha = hashlib.sha1()
        file.seek(0)
        sha.update(file.read())
        sha1 = sha.hexdigest()
        file.seek(0)

        return sha1
    
    except Exception, e:
        print e
        return None