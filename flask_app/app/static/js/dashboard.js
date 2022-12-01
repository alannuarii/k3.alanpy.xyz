const targetBPP = document.querySelectorAll(".need-comma");

for (comma of targetBPP) {
  const targetWithComma = parseInt(comma.innerText.slice(0, -7)).toLocaleString();
  comma.textContent = `${targetWithComma} Rp/kWh`;
}
