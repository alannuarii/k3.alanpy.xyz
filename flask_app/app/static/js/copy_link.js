// const copyButton = document.querySelectorAll(".btn-copy");
// const copyText = document.querySelectorAll(".link");
// const checklist = document.querySelectorAll(".checklist span i");
// const closeButton = document.querySelectorAll(".btn-keluar");

const linkBtn = document.querySelectorAll(".bi-link");
const copyLink = document.querySelectorAll(".copy-link");
const btnUp = document.querySelectorAll(".btn-up");
const btnCopy = document.querySelectorAll(".bi-files");
const copyText = document.querySelectorAll(".link");

// linkBtn.addEventListener("click", (e) => {
//   console.log(e);
// });

for (let i = 0; i < linkBtn.length; i++) {
  linkBtn[i].addEventListener("click", (e) => {
    e.preventDefault();
    copyLink[i].style.display = "block";
  });

  btnCopy[i].addEventListener("click", (e) => {
    copyText[i].select();
    copyText[i].setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText[i].value);
    btnCopy[i].style.color = "#ffc451";
  });

  btnUp[i].addEventListener("click", (e) => {
    e.preventDefault();
    copyLink[i].style.display = "none";
    btnCopy[i].style.color = "#fff";
  });
}

// for (let i = 0; i < copyButton.length; i++) {
//   copyButton[i].addEventListener("click", (e) => {
//     e.preventDefault();
// copyText[i].select();
// copyText[i].setSelectionRange(0, 99999);
// navigator.clipboard.writeText(copyText[i].value);
//     checklist[i].style.visibility = "visible";
//   });

//   closeButton[i].addEventListener("click", (e) => {
//     e.preventDefault();
//     checklist[i].style.visibility = "hidden";
//   });
// }
