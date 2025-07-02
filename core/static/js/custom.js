document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-add-to-cart').forEach(button => {
      button.addEventListener('click', () => {
        const product_id = button.dataset.productId;
        addToCart(product_id);
      });

    });
});

function addToCart(product_id, quantity = 1) {
  $.ajax({
    url: window.cartAddProductUrlTemplate.replace('0', product_id),
    method: 'POST',
    data: {
      product_id: product_id,  // your backend expects this in POST
      quantity: quantity,
      csrfmiddlewaretoken: window.csrfToken
    },
    success: function() {
      alert('محصول به سبد خرید اضافه شد!');
      window.location.reload();
    },
    error: function(xhr) {
      alert('خطا در افزودن محصول به سبد خرید: ' + xhr.responseText);
      console.error(xhr.responseText);
    }
  });
}




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

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

