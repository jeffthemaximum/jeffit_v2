function vote(voteButton) {
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var $voteDiv = $(voteButton).parent().parent();
    var $data = $voteDiv.data();
    var direction_name = $(voteButton).attr('title');
    var vote_value = null;
    if (direction_name == "upvote") {
        vote_value = 1;
    } else if (direction_name == "downvote") {
        vote_value = -1;
    } else {
        return;
    }

    var doPost = $.post('/vote/', {
        what: $data.whatType,
        what_id: $data.whatId,
        vote_value: vote_value
    });

    doPost.done(function (response) {
        if (response.error == null) {
            var voteDiff = response.voteDiff;
            var $score = null;
            var $upvoteArrow = null;
            var $downArrow = null;
            if ($data.whatType == 'submission') {
                $score = $voteDiv.find("div.score");
                $upvoteArrow = $voteDiv.children("div").children('i.fa.fa-chevron-up');
                $downArrow = $voteDiv.children("div").children('i.fa.fa-chevron-down');
            } else if ($data.whatType == 'comment') {
                var $medaiDiv = $voteDiv.parent().parent();
                var $votes = $medaiDiv.children('div.media-left').children('div.vote').children('div');
                $upvoteArrow = $votes.children('i.fa.fa-chevron-up');
                $downArrow = $votes.children('i.fa.fa-chevron-down');
                $score = $medaiDiv.find('div.media-body:first').find("a.score:first");

            }

            // update vote elements

            if (vote_value == -1) {
                if ($upvoteArrow.hasClass("upvoted")) { // remove upvote, if any.
                    $upvoteArrow.removeClass("upvoted")
                }
                if ($downArrow.hasClass("downvoted")) { // Canceled downvote
                    $downArrow.removeClass("downvoted")
                } else {                                // new downvote
                    $downArrow.addClass("downvoted")
                }
            } else if (vote_value == 1) {               // remove downvote
                if ($downArrow.hasClass("downvoted")) {
                    $downArrow.removeClass("downvoted")
                }

                if ($upvoteArrow.hasClass("upvoted")) { // if canceling upvote
                    $upvoteArrow.removeClass("upvoted")
                } else {                                // adding new upvote
                    $upvoteArrow.addClass("upvoted")
                }
            }

            // update score element
            var scoreInt = parseInt($score.text());
            $score.text(scoreInt += voteDiff);
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function submitEvent(event, form) {
    event.preventDefault();
    var $form = form;
    var data = $form.data();
    url = $form.attr("action");
    commentContent = $form.find("textarea#commentContent").val();

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var doPost = $.post(url, {
        parentType: data.parentType,
        parentId: data.parentId,
        commentContent: commentContent
    });

    doPost.done(function (response) {
        var errorLabel = $form.find("span#postResponse");
        if (response.msg) {
            errorLabel.text(response.msg);
            errorLabel.removeAttr('style');
        }
    });
}

$("#commentForm").submit(function (event) {
    submitEvent(event, $(this));
});

var newCommentForm = '<form id="commentForm" class="form-horizontal"\
                            action="/post/comment/"\
                            data-parent-type="comment">\
                            <fieldset>\
                            <div class="form-group comment-group">\
                                <label for="commentContent" class="col-lg-2 control-label">New comment</label>\
                                <div class="col-lg-10">\
                                    <textarea class="form-control" rows="3" id="commentContent"></textarea>\
                                    <span id="postResponse" class="text-success" style="display: none"></span>\
                                </div>\
                            </div>\
                            <div class="form-group">\
                                <div class="col-lg-10 col-lg-offset-2">\
                                    <button type="submit" class="btn btn-primary">Submit</button>\
                                </div>\
                            </div>\
                        </fieldset>\
                    </form>';


function buildEditCommentForm(originalComment) {
    var editCommentForm = '<form id="editCommentForm" class="form-horizontal"\
                            action="/post/editcomment/"\
                            data-parent-type="comment">\
                            <fieldset>\
                            <div class="form-group comment-group">\
                                <label for="commentContent" class="col-lg-2 control-label">Edit comment</label>\
                                <div class="col-lg-10">\
                                    <textarea class="form-control" rows="3" id="commentContent">'
                                    +originalComment+'</textarea>\
                                    <span id="postResponse" class="text-success" style="display: none"></span>\
                                </div>\
                            </div>\
                            <div class="form-group">\
                                <div class="col-lg-10 col-lg-offset-2">\
                                    <button type="submit" class="btn btn-primary">Submit</button>\
                                </div>\
                            </div>\
                        </fieldset>\
                    </form>';
    return editCommentForm;
}



$('a[name="replyButton"]').click(function () {
    var $mediaBody = $(this).parent().parent().parent();
    $(this).parent().parent().find("a[name=editButton]").toggle()
    if ($mediaBody.find('#commentForm').length == 0) {

        $mediaBody.parent().find(".reply-container:first").append(newCommentForm);
        var $form = $mediaBody.find('#commentForm');
        $form.data('parent-id', $mediaBody.parent().data().parentId);
        $form.submit(function (event) {
            submitEvent(event, $(this));
        });
    } else {
        $commentForm = $mediaBody.find('#commentForm:first');
        if ($commentForm.attr('style') == null) {
            $commentForm.css('display', 'none')
        } else {
            $commentForm.removeAttr('style')
        }
       //$(this).parent().parent().find("a[name=editButton]").show()
    }

});

function submitEditEvent(event, form) {
    event.preventDefault();
    var $form = form;
    var data = $form.data();
    url = $form.attr("action");
    editCommentContent = $form.find("textarea#commentContent").val();

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var doPost = $.post(url, {
        replyId: data.replyId,
        replyType: data.replyType,
        ancestorType: data.ancestorType,
        ancestorId: data.ancestorId,
        editCommentContent: editCommentContent
    });

    doPost.done(function (response) {
        var errorLabel = $form.find("span#postResponse");
        if (response.msg) {
            errorLabel.text(response.msg);
            errorLabel.removeAttr('style');
        }
    });
}

$("#editCommentForm").submit(function (event) {
    submitEditEvent(event, $(this));
});

var storedHTML = '';

$('a[name="editButton"]').click(function () {
    var $mediaBody = $(this).closest('.media-body');
    if ($mediaBody.find('#editCommentForm').length == 0) {
        $(this).parent().parent().find("a[name=replyButton]").hide()
        // find and store contents of comment
        var originalCommentText = $mediaBody.find('.commment-holder').html().replace(/ /g,'');
        //store original html
        storedHTML = originalCommentText;
        // convert originalCommentText to markdown
        originalCommentText = toMarkdown(originalCommentText);
        storedText = originalCommentText;
        // replace originalCommentText with form to edit it, prepopulated with originalCommentText
        var editCommentForm = buildEditCommentForm(originalCommentText);
        $mediaBody.find('.commment-holder').html(editCommentForm);
        var $form = $mediaBody.find('#editCommentForm');
        var replyId = $mediaBody.data().parentId;
        var replyType = $mediaBody.data().parentType;
        var ancestorType = $mediaBody.data().ancestor;
        var ancestorId = $mediaBody.data().ancestorId;
        $form.data('reply-id', replyId);
        $form.data('reply-type', replyType);
        $form.data('ancestor-type', ancestorType);
        $form.data('ancestor-id', ancestorId);
        $form.submit(function (event) {
            $(this).parent().parent().find("a[name=editButton]").toggle()
            submitEditEvent(event, $(this));
        });
    } else {
        var originalCommentText = $mediaBody.find('#editCommentForm').find("textarea#commentContent").val();
        $editCommentForm = $mediaBody.find('#editCommentForm:first');
        if ($editCommentForm.attr('style') == null) {
            $editCommentForm.css('display', 'none')
        } else {
            $editCommentForm.removeAttr('style')
        }
        $mediaBody.find('.commment-holder').html(marked(storedHTML));
        $(this).parent().parent().find("a[name=replyButton]").show()
    }
});


function removeOptionFromUrl() {
    var url = $(location).attr('href');
    var option = url.substr(url.length - 8, 7);
    var options = ['option1', 'option2', 'option3']
    if (options.indexOf(option) >= 0) {
        url = url.substr(0, url.length - 8);
    }
    return url;
}

// get sort buttons on leaderboard when clicked
$("input[name='options']").change(function(){
    var sortOption = this.id;
    var url = removeOptionFromUrl() + this.id;
    window.location.href = url;
})

function getOptionFromUrl() {
    var url = $(location).attr('href');
    var option = url.substr(url.length - 8, 7);
    return option;
}

$(document).ready(function(){
    var option = getOptionFromUrl();
    var options = ['option1', 'option2', 'option3']
    if (options.indexOf(option) >= 0) {
        $("input[id='"+option+"']").parent().attr('class', 'btn btn-primary btn-sm active');
    } else {
        $("input[id='option1']").parent().attr('class', 'btn btn-primary btn-sm active');
    }
});



