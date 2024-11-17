var users = [{ name: "ianpirro" }, { name: "joeschmoe" }, { name: "superdev" }];

var loginform = {
  init: function () {
    this.bindUserBox();
  },

  bindUserBox: function () {
    var $loginWrap = $("div.login-wrap");

    $(".form").on("blur", "input[name='un']", function () {
      var $self = $(this);

      var result = $.grep(users, function (elem) {
        return elem.name == $self.val();
      });

      if (result.length === 1) {
        if ($loginWrap.hasClass("register")) {
          loginform.revertForm();
          return;
        } else {
          return;
        }
      }

      if (!$loginWrap.hasClass("register")) {
        if ($self.val().length > 4) loginform.switchForm();
      }
    });
  },

  switchForm: function () {
    var $html = $("div.login-wrap").addClass("register");
    $html.children("h2").html("Register");
    $html
      .find(".form input[name='pw']")
      .after(
        "<input type='password' placeholder='Re-type password' name='rpw' />"
      );
    $html.find("button").html("Sign up");
    $html.find("a p").html("Have an account? Sign in");
  },

  revertForm: function () {
    var $html = $("div.login-wrap").removeClass("register");
    $html.children("h2").html("Login");
    $html.find(".form input[name='rpw']").remove();
    $html.find("button").html("Sign in");
    $html.find("a p").html("Don't have an account? Register");
  },

  submitForm: function () {
    // Aquí puedes agregar lógica para el envío del formulario, como una llamada AJAX.
  }
}; // loginform {}

// Inicializa el formulario de login
loginform.init();

// Alineación vertical usando Flexbox (CSS)
$(window).resize(function () {
  $(".login-wrap").css(
    "margin-top",
    Math.floor($(window).height() / 2 - $(".login-wrap").height() / 2)
  );
});

$(document).ready(function() {
  var images = [
    "http://127.0.0.1:8000/static/img/vet.jpg",
    "http://127.0.0.1:8000/static/img/vet2.jpeg",
    "http://127.0.0.1:8000/static/img/vet3.jpg",
    "http://127.0.0.1:8000/static/img/vet4.jpg"
  ];
  var currentIndex = 0;

  function changeBackground() {
    $("body::before").css("opacity", "0"); // Desvanece la imagen actual
    setTimeout(function() {
      currentIndex = (currentIndex + 1) % images.length;
      $("body::before").css("background-image", "url(" + images[currentIndex] + ")");
      $("body::before").css("opacity", "1"); // Aparece la nueva imagen
    }, 1000); // Espera 1 segundo (tiempo del fade out) antes de cambiar la imagen
  }

  setInterval(changeBackground, 5000); // Cambia la imagen cada 5 segundos
});