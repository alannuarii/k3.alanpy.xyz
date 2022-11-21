const penManager = document.querySelectorAll(".pen-manager");
const penK3L = document.querySelectorAll(".pen-k3l");
const titleSign = document.querySelector(".title-sign");
const role = document.querySelector(".role");
const can = document.querySelector(".sign-pad");
const sign = document.querySelector(".sign");

for (i = 0; i < penManager.length; i++) {
  penManager[i].addEventListener("click", (e) => {
    e.preventDefault();
    titleSign.innerText = "Manager";
    role.value = "manager";

    const signaturePad = new SignaturePad(can, {
      backgroundColor: "rgb(255, 255, 255)", // necessary for saving image as JPEG; can be removed is only saving as PNG or SVG
    });

    document.getElementById("submit").addEventListener("click", function () {
      if (signaturePad.isEmpty()) {
        return alert("Please provide a signature first.");
      }

      const data = signaturePad.toDataURL("image/png");
      sign.value = data;
    });

    document.getElementById("clear").addEventListener("click", function () {
      signaturePad.clear();
    });
  });

  penK3L[i].addEventListener("click", (e) => {
    e.preventDefault();
    titleSign.innerText = "Pejabat K3L dan Kam";
    role.value = "k3l";

    const signaturePad = new SignaturePad(can, {
      backgroundColor: "rgb(255, 255, 255)", // necessary for saving image as JPEG; can be removed is only saving as PNG or SVG
    });

    document.getElementById("submit").addEventListener("click", function () {
      if (signaturePad.isEmpty()) {
        return alert("Please provide a signature first.");
      }

      const data = signaturePad.toDataURL("image/png");
      sign.value = data;
    });

    document.getElementById("clear").addEventListener("click", function () {
      signaturePad.clear();
    });
  });
}
