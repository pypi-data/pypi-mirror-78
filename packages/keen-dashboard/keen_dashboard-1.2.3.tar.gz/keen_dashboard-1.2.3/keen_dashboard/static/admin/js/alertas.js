function alertaSucesso(mensagem)
{
    swal.fire({
      type: "success",
      title: mensagem,
      showConfirmButton: false,
      timer: 1500,
    });
}

function alertaErro(mensagem)
{
    swal.fire({
      type: 'error',
      title: 'Oops...',
      text: mensagem,
    });
}

function alertaGenerico(json)
{
    swal.fire({
      type: json.icon,
      title: json.mensagem,
      showConfirmButton: false,
      timer: 1500,
    });
}

(function($) {
    $('[data-confirm]').click( function() {
        let element = $(this)
        event.preventDefault();
        let text = element.attr('data-confirm-text')
        let icon = element.attr('data-confirm-icon')
        let title = element.attr('data-confirm-title')
        let button_text = element.attr('data-confirm-button-text')

        swal.fire({
              title: title,
              text: text,
              type: icon,
              showCancelButton: true,
              confirmButtonColor: '#5398fb',
              cancelButtonColor: '#fa6767',
              confirmButtonText: button_text,
              cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                location.href = element.attr('href')
            }
        });

    });
})(jQuery);