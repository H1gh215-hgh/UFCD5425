// ===========================================================
// TarefaFácil — app.js
// Pequenos comportamentos no lado do cliente:
// confirmação antes de eliminar e desaparecimento automático
// das mensagens de aviso.
// ===========================================================

document.addEventListener("DOMContentLoaded", function () {
  // Pede confirmação antes de submeter formulários marcados
  // com o atributo "data-confirmar".
  const formulariosComConfirmacao = document.querySelectorAll("[data-confirmar]");
  formulariosComConfirmacao.forEach(function (formulario) {
    formulario.addEventListener("submit", function (evento) {
      const mensagem = formulario.getAttribute("data-confirmar") || "Tem a certeza?";
      if (!window.confirm(mensagem)) {
        evento.preventDefault();
      }
    });
  });

  // Faz as mensagens de aviso (flash) desaparecerem sozinhas
  // depois de alguns segundos.
  const mensagens = document.querySelectorAll(".mensagem");
  mensagens.forEach(function (mensagem) {
    setTimeout(function () {
      mensagem.style.transition = "opacity 0.5s ease";
      mensagem.style.opacity = "0";
      setTimeout(function () {
        mensagem.remove();
      }, 500);
    }, 4000);
  });
});
