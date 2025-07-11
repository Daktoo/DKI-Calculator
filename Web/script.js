const display = document.getElementById("display");
const buttonsDiv = document.getElementById("buttons");

let expr = "";
let memVal = null;
let snipHist = [];

// gonna add more buttons soon
const buttons = [
  "7", "8", "9", "+", "-", "C",
  "4", "5", "6", "*", "/", "^",
  "1", "2", "3", "(", ")", "=",
  "0", ".", "π", "e", "√", "log",
  "sin", "cos", "tan", "ln", "Frac", "Frac-Dec",
  "M+", "MR", "MC", "H"
];

buttons.forEach(label => {
  const btn = document.createElement("button");
  btn.textContent = label;
  btn.onclick = function() {
    handleBtn(label);
  };
  buttonsDiv.appendChild(btn);
});

// Handles all button presses
function handleBtn(label) {
  if (label === "C") {
    expr = "";
    display.value = "";
  } 
  
  else if (label === "=") {
    calculate();
  } 
  
  else if (label === "Frac-Dec") {
    convertToFraction();
  } 
  
  else if (label === "M+") {
    memVal = safeEval(expr);
    display.value = `Saved: ${memVal}`;
  } 
  
  else if (label === "MR") {
    if (memVal !== null) {
      expr += memVal;
      display.value = expr;
    }
  } 
  
  else if (label === "MC") {
    memVal = null;
    display.value = "Memory cleared";
  } 
  
  else if (label === "H") {
    display.value = snipHist.slice(-3).join(" | ") || "No history";
  } 
  
  else if (label === "π") {
    expr += Math.PI;
    display.value = expr;
  } 
  
  else if (label === "e") {
    expr += Math.E;
    display.value = expr;
  } 
  
  else if (label === "√") {
    expr += "Math.sqrt(";
    display.value = expr;
  } 
  
  else if (label === "log") {
    expr += "Math.log10(";
    display.value = expr;
  } 
  
  else if (label === "ln") {
    expr += "Math.log(";
    display.value = expr;
  } 
  
  else if (["sin", "cos", "tan"].includes(label)) {
    expr += `Math.${label}(`;
    display.value = expr;
  } 
  
  else if (label === "^") {
    expr += "**";  
    display.value = expr;
  } 
  
  else if (label === "Frac") {
    expr += "frac("; 
    display.value = expr;
  } 
  
  else {
    expr += label;
    display.value = expr;
  }
}

// Main calc function
function calculate() {
  // fun easter egg :D
  if (expr.replace(/\s/g, "") === "28/08" || expr.replace(/\s/g, "") === "28/8") {
    display.value = "It's me!";
    let img = new Image();
    img.src = "dak.png";
    img.style.maxWidth = "100%";
    img.onload = function() {
      buttonsDiv.innerHTML = "";  // nuke buttons, show pic
      buttonsDiv.appendChild(img);
    };
    expr = "";
    return;
  }

  try {
    const res = safeEval(expr); // eval ftw
    display.value = res;
    snipHist.push(`${expr} = ${res}`);
    expr = res.toString();
  } catch (err) {
    display.value = "Error";
    expr = "";
  }
}

// decimal to fraction function
function convertToFraction() {
  try {
    const val = safeEval(expr);
    const f = toFraction(val);
    display.value = f;
    expr = f;
  } catch (oops) {
    display.value = "Error";
  }
}

// Fraction conversion
function toFraction(decimal) {
  let tolerance = 1.0e-6;
  let h1 = 1, h2 = 0, k1 = 0, k2 = 1;
  let b = decimal;

  do {
    let a = Math.floor(b);
    let temp = h1;
    h1 = a * h1 + h2;
    h2 = temp;

    temp = k1;
    k1 = a * k1 + k2;
    k2 = temp;

    b = 1 / (b - a);
  } while (Math.abs(decimal - h1 / k1) > decimal * tolerance);

  return h1 + "/" + k1;
}

// just a quick wrapper
function safeEval(expression) {
  return Function('"use strict"; return (' + expression + ')')();
}
