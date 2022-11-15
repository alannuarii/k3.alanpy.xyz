const copyButton = document.querySelectorAll(".btn-copy");
const copyText = document.querySelectorAll(".link");
const checklist = document.querySelectorAll(".checklist span i");
const closeButton = document.querySelectorAll(".btn-keluar");

for (let i = 0; i < copyButton.length; i++) {
  copyButton[i].addEventListener("click", (e) => {
    e.preventDefault();
    copyText[i].select();
    copyText[i].setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText[i].value);
    checklist[i].style.visibility = "visible";
  });

  closeButton[i].addEventListener("click", (e) => {
    e.preventDefault();
    checklist[i].style.visibility = "hidden";
  });
}
