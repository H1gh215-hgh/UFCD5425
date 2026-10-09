// ContactosFácil — app.js
// Guarda os contactos no localStorage do navegador (sem servidor, sem base de dados)

// Vai buscar os contactos já guardados no navegador (ou começa com uma lista vazia)
let contactos = JSON.parse(localStorage.getItem("contactos")) || [];

// Elementos da página que vamos usar várias vezes
const formulario = document.getElementById("formulario");
const lista = document.getElementById("lista");
const listaVazia = document.getElementById("listaVazia");
const contador = document.getElementById("contador");
const mensagemErro = document.getElementById("mensagemErro");

// Corre assim que a página abre, para mostrar os contactos já guardados
mostrarContactos();

// Quando o formulário é submetido (botão clicado ou tecla Enter), adiciona o contacto
formulario.addEventListener("submit", function (evento) {
  evento.preventDefault();
  adicionarContacto();
});

function adicionarContacto() {
  const nome = document.getElementById("nome").value.trim();
  const telefone = document.getElementById("telefone").value.trim();
  const email = document.getElementById("email").value.trim();

  if (nome === "") {
    mostrarErro("Escreva pelo menos um nome antes de adicionar o contacto.");
    return;
  }

  contactos.push({ nome: nome, telefone: telefone, email: email });
  guardar();
  mostrarContactos();
  limparFormulario();
  esconderErro();
}

function guardar() {
  localStorage.setItem("contactos", JSON.stringify(contactos));
}

function mostrarContactos() {
  lista.innerHTML = "";

  contactos.forEach(function (contacto, indice) {
    const item = document.createElement("li");
    item.className = "contacto";

    const detalhes = [contacto.telefone, contacto.email].filter(Boolean).join(" · ");

    item.innerHTML =
      '<div class="contacto-info">' +
        '<span class="contacto-nome">' + escaparTexto(contacto.nome) + "</span>" +
        (detalhes ? '<span class="contacto-detalhe">' + escaparTexto(detalhes) + "</span>" : "") +
      "</div>" +
      '<button class="botao-apagar" onclick="apagar(' + indice + ')">Apagar</button>';

    lista.appendChild(item);
  });

  listaVazia.hidden = contactos.length > 0;
  contador.textContent = contactos.length + (contactos.length === 1 ? " contacto" : " contactos");
}

function apagar(indice) {
  contactos.splice(indice, 1);
  guardar();
  mostrarContactos();
}

function limparFormulario() {
  formulario.reset();
  document.getElementById("nome").focus();
}

function mostrarErro(texto) {
  mensagemErro.textContent = texto;
  mensagemErro.hidden = false;
}

function esconderErro() {
  mensagemErro.hidden = true;
}

// Evita que texto escrito pelo utilizador seja interpretado como HTML
function escaparTexto(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}
