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
    $toggleFilter.trigger("click");
});

function toggleChoiceList($filterLink, $choiceList) {
    isHidden = $choiceList.hasClass('hide');
    hasSelected = $choiceList
                    .children()               // Get choices 
                    .slice(1)                 // Ignores the first choice, which is the 'All' selection
                    .hasClass('selected');

    if (isHidden) {
        $choiceList.removeClass('hide');
        newText = $filterLink.html().replace("Show","Hide");
        $filterLink.html(newText);
    }
    else {
        $choiceList.addClass('hide');
        newText = $filterLink.html().replace("Hide","Show");
        $filterLink.html(newText);
        if (hasSelected) {
            $filterLink
                .find('.filter-title')
                .addClass('selected')
        }
    }
}


