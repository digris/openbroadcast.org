from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.uploadedfile import UploadedFile

from models import MultiuploaderImage


#importing json parser to generate jQuery plugin friendly json response
import json

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
#from sorl.thumbnail import get_thumbnail


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    
    result = []
    
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))
        log.info('Content type: "$s" % file.content_type')

        #writing file manually into model
        #because we don't need form of any type.
        image = MultiuploaderImage()
        image.filename=str(filename)
        image.image=file
        image.key_data = image.key_generate
        image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        if 'image' in file.content_type.lower():
            """
            #im = get_thumbnail(image, "80x80", quality=50)
            opt = dict(size=(80, 80), crop=True, bw=False, quality=80)
            im = get_thumbnailer(image).get_thumbnail(opt)
            thumb_url = im.url
            """
            thumb_url = ''
        else:
            thumb_url = ''

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        #generating json response array
        
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = json.dumps(result)
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')
    
    
    
    
    

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})