const display = document.getElementById("display");
    const buttonsDiv = document.getElementById("buttons");
    let expr = "";
    let memory = null;
    let history = [];

    const buttons = [
      "7", "8", "9", "+", "-", "C",
      "4", "5", "6", "*", "/", "^",
      "1", "2", "3", "(", ")", "=",
      "0", ".", "π", "e", "√", "log",
      "sin", "cos", "tan", "ln", "Frac", "Frac-Dec",
      "M+", "MR", "MC", "H"
    ];

    buttons.forEach((label) => {
      const btn = document.createElement("button");
      btn.textContent = label;
      btn.onclick = () => handleButton(label);
      buttonsDiv.appendChild(btn);
    });

    function handleButton(label) {
      if (label === "C") {
        expr = "";
        display.value = "";
      } else if (label === "=") {
        calculate();
      } else if (label === "Frac-Dec") {
        convertToFraction();
      } else if (label === "M+") {
        memory = safeEval(expr);
        display.value = `Saved: ${memory}`;
      } else if (label === "MR") {
        if (memory !== null) {
          expr += memory;
          display.value = expr;
        }
      } else if (label === "MC") {
        memory = null;
        display.value = "Memory cleared";
      } else if (label === "H") {
        display.value = history.slice(-3).join(" | ") || "No history";
      } else if (label === "π") {
        expr += Math.PI;
        display.value = expr;
      } else if (label === "e") {
        expr += Math.E;
        display.value = expr;
      } else if (label === "√") {
        expr += "Math.sqrt(";
        display.value = expr;
      } else if (label === "log") {
        expr += "Math.log10(";
        display.value = expr;
      } else if (label === "ln") {
        expr += "Math.log(";
        display.value = expr;
      } else if (["sin", "cos", "tan"].includes(label)) {
        expr += `Math.${label}(`;
        display.value = expr;
      } else if (label === "^") {
        expr += "**";
        display.value = expr;
      } else if (label === "Frac") {
        expr += "frac(";
        display.value = expr;
      } else {
        expr += label;
        display.value = expr;
      }
    }

    function calculate() {
      if (expr.replace(/\s/g, "") === "28/08" || expr.replace(/\s/g, "") === "28/8") {
        display.value = "It's me!";
        let img = new Image();
        img.src = "dak.png";
        img.style.maxWidth = "100%";
        img.onload = () => {
          buttonsDiv.innerHTML = "";
          buttonsDiv.appendChild(img);
        };
        expr = "";
        return;
      }

      try {
        const result = safeEval(expr);
        display.value = result;
        history.push(`${expr} = ${result}`);
        expr = result.toString();
      } catch (e) {
        display.value = "Error";
        expr = "";
      }
    }

    function convertToFraction() {
      try {
        const value = safeEval(expr);
        const frac = toFraction(value);
        display.value = frac;
        expr = frac;
      } catch {
        display.value = "Error";
      }
    }

    function toFraction(decimal) {
      let tolerance = 1.0e-6;
      let h1 = 1, h2 = 0, k1 = 0, k2 = 1, b = decimal;
      do {
        let a = Math.floor(b);
        let aux = h1;
        h1 = a * h1 + h2;
        h2 = aux;
        aux = k1;
        k1 = a * k1 + k2;
        k2 = aux;
        b = 1 / (b - a);
      } while (Math.abs(decimal - h1 / k1) > decimal * tolerance);
      return h1 + "/" + k1;
    }

    function safeEval(expression) {
      return Function('"use strict"; return (' + expression + ')')();
}