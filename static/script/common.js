$(document).ready(function() {
    setTimeout(function() {
        $('messages').fadeOut(1000, function() {
            $(this).remove()
        })
    }, 4000)
    $('a#burger').on('click', function() {
        let nav = $('span#navigation')
        if (nav.css('visibility') !== 'collapse') {
            nav.css('visibility', 'collapse')
        } else {
            nav.css('visibility', 'visible')
        }
    })
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