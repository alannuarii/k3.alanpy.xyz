const down = document.querySelector(".bi-chevron-double-down");

// function agendaToggle() {
//   down.classList.toggle("bi-chevron-double-right");
// }

down.addEventListener("click", () => {
  down.classList.toggle("bi-chevron-double-up");
});
