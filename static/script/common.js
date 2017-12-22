'use strict'

$(document).ready(function() {
    /* hide flashed messages after a while with a fadeout effect */
    setTimeout(function() {
        $('messages').fadeOut(1000, function() {
            $(this).remove()
        })
    }, 4000)
    /* use the burger button to toggle menu options visibility on mobile */
    $('a#burger').on('click', function() {
        let nav = $('span#navigation')
        if (nav.css('visibility') !== 'collapse') {
            nav.css('visibility', 'collapse')
        } else {
            nav.css('visibility', 'visible')
        }
    })
    /* reveal or hide the menu options when window size changes */
    $(window).on('resize', function() {
        let nav = $('span#navigation')
        let winwidth = $(this).width()
        if (winwidth > 800 && nav.css('visibility') !== 'visible') {
            nav.css('visibility', 'visible')
        } else if (winwidth <= 800 && nav.css('visibility') !== 'collapse') {
            nav.css('visibility', 'collapse')
        }
    })
})