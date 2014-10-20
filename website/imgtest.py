

filename = 'test.jpg'
file = ''

folder = Folder.objects.get(name='01574266-d9ab-11e1-ba53-b8f6b11a3aed')

print folder

obj, created = Image.objects.get_or_create(
                                original_filename=filename,
                                file=file,
                                folder=folder,
                                is_public=True)