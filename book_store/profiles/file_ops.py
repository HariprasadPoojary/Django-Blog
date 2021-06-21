def save_file(file):
    """
    Function to save file in .jpg format in "files" directory
    """
    with open("files/photo.jpg", "wb+") as ops:
        for chunk in file.chunks():
            ops.write(chunk)