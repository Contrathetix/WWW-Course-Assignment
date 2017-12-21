$(document).ready(function() {
    setTimeout(function() {
        $('messages').fadeOut(1000, function() {
            $(this).remove()
        })
    }, 4000)
})