var common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';
jq(function(){
    function noformerrorshow(el, noform) {
        var o = jq(el),
            emsg = o.find('dl.portalMessage.error');
        if (emsg.length) {
            o.children().replaceWith(emsg);
            return false;
        } else {
            return noform;
        }
    }
    var base_url = jq('base').attr('href').split('/');
    var cutted = base_url.splice(-2,2); // cut off last two elements
    jq('.portletBillboardActions ul a#deleteentry').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: base_url.join('/'),
            closeselector: '[name=form.button.Cancel]',
            width:'50%'
        }
    );
    var upload_url = jq('base').attr('href').split('/');
    cutted = upload_url.splice(-1,1); // cut off last element
    jq('.portletBillboardActions ul a#uploadimage').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: upload_url.join('/'),
            closeselector: '[name=form.button.Cancel]',
            width:'50%'
        }
    );
    base_url = jq('base').attr('href').split('/');
    cutted = base_url.splice(-1,1); // cut off last element
    jq('a.deleteImage').prepOverlay(
        {
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form',
            noform: function(el) {return noformerrorshow(el, 'redirect');},
            redirect: base_url.join('/'),
            closeselector: '[name=form.button.Cancel]',
            width:'50%'
        }
    );
    jq('.overlayImage').prepOverlay({
        subtype: 'image'
    });
});