if (!$) {
    $ = django.jQuery;
}

$(document).ready(function() {
    $toggleFilter = $('.js-toggle-filter');
    $filters = $('#changelist-filter');
    $choiceList = $filters.find('.choice-list');
    // Add click events
    $toggleFilter.click(function(evt) {
        toggleChoiceList($(this), $(this).next());
    });
    // Hide filters on load
    $toggleFilter.each(function(i, filterLink) {        
        $choiceList = $(filterLink).next();        
        hideList($(filterLink), $choiceList);
    });
        
});

function toggleChoiceList($filterLink, $choiceList) {    
    isHidden = $choiceList.hasClass('hide');
    if (isHidden) { showList($filterLink, $choiceList) }
    else          { hideList($filterLink, $choiceList) }
}

function showList ($filterLink, $choiceList) {
    $choiceList.removeClass('hide');
    newText = $filterLink.html().replace("Show","Hide");
    $filterLink.html(newText);
}

function hideList($filterLink, $choiceList) {
    hasSelected = $choiceList
                    .children()               // Get choices 
                    .slice(1)                 // Ignores the first choice, which is the 'All' selection
                    .hasClass('selected');
                    
    $choiceList.addClass('hide');
    newText = $filterLink.html().replace("Hide","Show");
    $filterLink.html(newText);
    if (hasSelected) {
        $filterLink
            .find('.filter-title')
            .addClass('selected')
    }
}
