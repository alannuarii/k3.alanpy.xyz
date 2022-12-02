const down = document.querySelector(".bi-chevron-double-down");
const kondisiDown = document.querySelectorAll("#dashboard .bi-chevron-double-down");

down.addEventListener("click", () => {
  down.classList.toggle("bi-chevron-double-up");
});

for (let i = 1; i < kondisiDown.length; i++) {
  kondisiDown[i].addEventListener("click", () => {
    kondisiDown[i].classList.toggle("bi-chevron-double-up");
  });
}
