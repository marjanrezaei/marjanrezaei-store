function changePage(page_number){
  let current_url_params = new URLSearchParams(window.location.search)
  current_url_params.set('page', page_number)
  let new_url = window.location.pathname + "?" + current_url_params.toString()
  window.location.href = new_url
}

function fromatPriceInToman(element) {
  let rawPrice = parseFloat(element.innerText);
  let formatter = new Intl.NumberFormat('fa-IR');
  let formattedPrice = formatter.format(rawPrice);
  element.innerText = `${formattedPrice} تومان`; 
}

document.addEventListener("DOMContentLoaded", function(){
  let priceElements = document.querySelectorAll('.formatted-price');
  priceElements.forEach(element => fromatPriceInToman(element));
});


function changeProductQuantity(product_id, quantity) {
  $.ajax({
    url: window.cartUpdateUrl,
    method: 'POST',
    data: {
      product_id: product_id,
      quantity: quantity,
      csrfmiddlewaretoken: window.csrfToken
    },
    success: function(response) {
      console.log('Quantity updated:', response);
      window.location.reload();
    },
    error: function(xhr) {
      console.error('Failed to update quantity', xhr);
    }
  });
}


function removeProduct(product_id) {
  $.ajax({
    url: window.removeUrl,
    method: 'POST',
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: window.csrfToken
    },
    success: function(response) {
      console.log(response);
      window.location.reload();
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log(errorThrown);
    }
  });
}
