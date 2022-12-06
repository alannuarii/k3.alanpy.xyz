const targetBPP = document.querySelectorAll(".need-comma");

for (comma of targetBPP) {
  const targetWithComma = parseInt(comma.innerText.slice(0, -7)).toLocaleString();
  comma.textContent = `${targetWithComma} Rp/kWh`;
}


const giveComma = document.querySelectorAll('.comma');

for (comma of giveComma){
  const convert = parseInt(comma.innerText).toLocaleString()
  comma.textContent = convert
}