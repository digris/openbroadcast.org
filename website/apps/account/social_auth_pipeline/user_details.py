from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def get_details(
    backend, strategy, details, response, user=None, *args, **kwargs
):

    if not user:
        return

    changed = False
    #
    # if backend.name == "vk-oauth2":
    #
    #     if not user.first_name and "first_name" in response:
    #         user.first_name = response["first_name"]
    #         changed = True
    #
    #     if not user.last_name and "last_name" in response:
    #         user.last_name = response["last_name"]
    #         changed = True
    #
    #
    #     # the image
    #     if not user.images.exists():
    #
    #         try:
    #
    #             from account.models import UserImage
    #
    #             img_url = response["photo"][0]
    #
    #             img_temp = NamedTemporaryFile(delete=True)
    #             img_temp.write(urlopen(img_url).read())
    #             img_temp.flush()
    #
    #             i = UserImage(co=user)
    #             i.save()
    #
    #             i.file.save("img_{}".format(i.uuid), File(img_temp))
    #
    #             changed = True
    #
    #         except Exception as e:
    #             print("error getting image: {} - {}".format(backend.name, e))
    #             pass
    #
    # if backend.name == "spotify":
    #
    #     if not user.full_name and "display_name" in response:
    #         user.full_name = response["display_name"]
    #         changed = True
    #
    #     # the image
    #     if not user.images.exists():
    #
    #         try:
    #
    #             from account.models import UserImage
    #
    #             img_url = response["images"][0]["url"]
    #
    #             img_temp = NamedTemporaryFile(delete=True)
    #             img_temp.write(urlopen(img_url).read())
    #             img_temp.flush()
    #
    #             i = UserImage(co=user)
    #             i.save()
    #
    #             i.file.save("img_{}".format(i.uuid), File(img_temp))
    #
    #             changed = True
    #
    #         except Exception as e:
    #             print("error getting image: {} - {}".format(backend.name, e))
    #             pass
    #
    # if backend.name == "facebook":
    #
    #     if not user.full_name and "name" in response:
    #         user.full_name = response["name"]
    #         changed = True
    #
    #     # the image
    #     if not user.images.exists():
    #
    #         try:
    #
    #             from account.models import UserImage
    #
    #             img_url = "http://graph.facebook.com/{}/picture?type=large".format(
    #                 response["id"]
    #             )
    #
    #             img_temp = NamedTemporaryFile(delete=True)
    #             img_temp.write(urlopen(img_url).read())
    #             img_temp.flush()
    #
    #             i = UserImage(co=user)
    #             i.save()
    #
    #             i.file.save("img_{}".format(i.uuid), File(img_temp))
    #
    #             changed = True
    #
    #         except Exception as e:
    #             print("error getting image: {} - {}".format(backend.name, e))
    #             pass

    if backend.name == "google-oauth2":


        print(response)

        if not user.first_name and "given_name" in response:
            user.first_name = response["given_name"]
            changed = True

        if not user.last_name and "family_name" in response:
            user.last_name = response["family_name"]
            changed = True

        #
        # if (
        #     "image" in response
        #     and response["image"]
        #     and not user.images.exists()
        # ):
        #
        #     try:
        #
        #         from account.models import UserImage
        #
        #         img_url = response["image"]["url"].split("?")[0]
        #
        #         img_temp = NamedTemporaryFile(delete=True)
        #         img_temp.write(urlopen(img_url).read())
        #         img_temp.flush()
        #
        #         i = UserImage(co=user)
        #         i.save()
        #
        #         i.file.save("img_{}".format(i.uuid), File(img_temp))
        #
        #         changed = True
        #
        #     except Exception as e:
        #         print("error getting image: {} - {}".format(backend.name, e))
        #         pass

    if changed:
        strategy.storage.user.changed(user)
