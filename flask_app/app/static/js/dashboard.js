const targetBPP = document.querySelector(".target").childNodes[3].innerText;

console.log(parseInt(targetBPP.slice(0,-7)).toLocaleString());
