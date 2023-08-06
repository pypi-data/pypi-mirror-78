(function ($) {
    'use strict';

    $("#changelist-table tbody tr").click(handleTdClick);
    $("#changelist-table tbody tr").dblclick(handleDblClick);


    function handleTdClick(e) {
        if (parent != window) {
            let frame_element = $(frameElement);
            let parent_input = '#' + frame_element.attr('id').replace('iframe_', '');
            let search_field = frame_element.data('search-field');

            var valor = '';
            if (search_field !== 'action-select') {
                let search_value = $(this).find('.field-' + search_field).first();
                valor = search_value.text();
            } else {
                let search_value = $(this).find('.' + search_field).first();
                valor = search_value.val();
            }

            parent.$('.modal').modal('hide');
            let parent_input_element = parent.$(parent_input);
            parent_input_element.val(valor);
            parent_input_element.trigger('change');

        }
        return true;
    }

    function handleDblClick(e) {
        $(this).find("a").first()[0].click();
    }

})(jQuery);