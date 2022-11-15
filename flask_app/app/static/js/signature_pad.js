var canvas = document.getElementById("signature-pad");
var ttd = document.getElementById("ttd");

var signaturePad = new SignaturePad(canvas, {
  backgroundColor: "rgb(255, 255, 255)", // necessary for saving image as JPEG; can be removed is only saving as PNG or SVG
});

document.getElementById("submit").addEventListener("click", function () {
  if (signaturePad.isEmpty()) {
    return alert("Please provide a signature first.");
  }

  var data = signaturePad.toDataURL("image/png");
  ttd.value = data
});

document.getElementById("clear").addEventListener("click", function () {
  signaturePad.clear();
});
