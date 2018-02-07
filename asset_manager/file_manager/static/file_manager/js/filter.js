if (!$) {
    $ = django.jQuery;
}

$(document).ready(function() {
    $toggleFilter = $('.js-toggle-filter');
    $filters = $('#changelist-filter');
    $choiceList = $filters.find('.choice-list');

    $toggleFilter.click(function(evt) {
        toggleChoiceList($(this), $(this).next());
    });
});

function toggleChoiceList($filterLink, $choiceList) {
    isHidden = $choiceList.hasClass('hide');

    if (isHidden) {
        $choiceList.removeClass('hide');
        newText = $filterLink.html().replace("Show","Hide");
        $filterLink.html(newText);
    }
    else {
        $choiceList.addClass('hide');
        newText = $filterLink.html().replace("Hide","Show");
        $filterLink.html(newText);
    }
}


