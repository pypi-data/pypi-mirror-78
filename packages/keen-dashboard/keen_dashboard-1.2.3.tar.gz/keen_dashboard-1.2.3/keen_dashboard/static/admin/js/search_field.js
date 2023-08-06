(function($) {
    'use strict';

    // Global for testing purposes
    $(document).ready(function() {

        $("a[data-popup-opener]").on('click', function(event) {
            event.preventDefault();
            opener.dismissRelatedLookupPopup(window, $(this).data("popup-opener"));
        });

        $('body').on('click', '.related-widget-wrapper-link', function(e) {
            e.preventDefault();
            if (this.href) {
                var event = $.Event('django:show-related', {href: this.href});
                $(this).trigger(event);
                if (!event.isDefaultPrevented()) {
                    showRelatedObjectPopup(this);
                }
            }
        });

        $('body').on('change', '.related-widget-wrapper select', function(e) {
            var event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                updateRelatedObjectLinks(this);
            }
        });

        $('.related-widget-wrapper select').trigger('change');
        $('body').on('click', '[data-search]', function(e) {
            e.preventDefault();
            var event = $.Event('django:lookup-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                let id_search = $(this).attr('id').replace('lookup_', '')
                $('#iframe_' + id_search).attr('src', $(this).attr('href'));
                $('#modal_' + id_search).modal('show');
            }
        });
    });

})(jQuery);
