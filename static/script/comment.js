'use strict'

// create and append new comment to the page
function createComment(username, content) {
    jQuery('<span/>', {class: 'comment'}).append(
        jQuery('<p/>', {text: username}),
        jQuery('<p/>', {text: content})
    ).insertAfter('main > h1:nth-of-type(2)').hide().fadeIn(400)
}

/* Fetch comments for the image from the server using ajax. */
function updateComments() {
    $('span.comment').fadeOut(400, function() {
        $(this).remove()
    })
    let imageuuid = window.location.pathname.match(/image\/(.*)\/$/)[1]
    //console.log(imageuuid)
    let requesturl = '/action/get-comments/' + imageuuid + '/'
    //console.log(requesturl)
    $.getJSON(requesturl, function(responsedata) {
        console.log(responsedata)
        for (let i=0; i<responsedata.length; i++) {
            createComment(responsedata[i]['username'], responsedata[i]['comment'])
        }
        setTimeout(updateComments, 5000)
    })
}

$(document).ready(function() {

    updateComments() // initiate the comment update cycle to the background

    /* Override comment submission form functionality to work with ajax instead */
    $('form#commentsubmission').on('submit', function(event) {
        event.preventDefault()
        // get data fields, excluding the 'submit' button
        let fields = $(this).find('input[type!=submit]')
        let data = {}
        for (let i=0; i<fields.length; i++) {
            // map values for sending to the server
            data[$(fields[i]).attr('name')] = $(fields[i]).val()
        }
        // send the new comment to server, check if the submission was a success
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: JSON.stringify(data),
            dataType: 'json'
        }).done(function(responsedata) {
            //console.log(responsedata)
            if (responsedata === true) {
                // adding comment was a success, add the comment among the existing ones
                createComment('(myself)', data['comment'])
            } else {
                alert('comment submission failed')
            }
        })
    })

})