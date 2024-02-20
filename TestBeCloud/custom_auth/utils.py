def user_directory_path(instance, filename):
    return 'user_images/{0}/{1}'.format(instance.user.id, filename)
