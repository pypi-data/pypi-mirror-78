window.onload = function () {

    jQuery(function ($) {
        $.fn.datepicker.dates['pt-BR'] = {
            days: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
            daysShort: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
            daysMin: ["Do", "2°", "3°", "4°", "5°", "6°", "Sa"],
            months: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                "Setembro", "Outubro", "Novembro", "Dezembro"],
            monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            today: "Hoje",
            clear: "Clear",
            titleFormat: "MM yyyy",
            weekStart: 0
        };

        $.fn.datetimepicker.dates['pt-BR'] = {
            days: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
            daysShort: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
            daysMin: ["Do", "2°", "3°", "4°", "5°", "6°", "Sa"],
            months: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto",
                "Setembro", "Outubro", "Novembro", "Dezembro"],
            monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            today: "Hoje",
            clear: "Clear",
            titleFormat: "MM yyyy",
            weekStart: 0
        };

        $('[datepicker-br]').datepicker({
            language: "pt-BR",
            weekHeader: 'Sm',
            orientation: "auto",
            todayBtn: true,
            titleFormat: "MM yyyy",
            format: "dd/mm/yyyy",
            weekStart: 0,
            onSelect: function() {
                $(this).change();
            }
        });

        $('[timepicker-br]').timepicker({
            showMeridian: false,
            showSeconds: true,
            onSelect: function() {
                $(this).change();
            }
        });

    });

};