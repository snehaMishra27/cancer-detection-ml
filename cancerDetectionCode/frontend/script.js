// function predict() {
//     const data = {
//         age: Number(document.getElementById("age").value),
//         num_partners: Number(document.getElementById("partners").value),
//         smokes: Number(document.getElementById("smokes").value),
//         stds: Number(document.getElementById("stds").value)
//     };

//     fetch("http://127.0.0.1:5000/predict", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(data)
//     })
//     .then(res => res.json())
//     .then(data => {
//         document.getElementById("result").innerText =
//             data.prediction === 1 ?
//             "⚠️ High Risk Detected" :
//             "✅ Low Risk Detected";
//     });
// }



// async function predict() {
//   const data = {
//     f1: Number(document.getElementById("f1").value),
//     f2: Number(document.getElementById("f2").value),
//     f3: Number(document.getElementById("f3").value),
//     f4: Number(document.getElementById("f4").value)
//   };

//   const response = await fetch("http://127.0.0.1:5000/predict", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//         f1: Number(f1),
//         f2: Number(f2),
//         f3: Number(f3),
//         f4: Number(f4)
//     })
//   });

//   const result = await response.json();
//   document.getElementById("result").innerText =
//     result.prediction === 1
//       ? "⚠️ High Risk of Cervical Cancer"
//       : "✅ Low Risk of Cervical Cancer";
// }


async function predict() {

  try{
    const age = document.getElementById("age").value;
    const partners = document.getElementById("partners").value;
    const smokes = document.getElementById("smokes").value;
    const stds = document.getElementById("stds").value;
    const dx= document.getElementById("dx").value;
    

    if (age === "" || partners === "" || smokes === "" || stds === "" || dx==="") {
      alert("Please fill all fields");
      return;
    }
    const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "Age": Number(age),
        "Number of sexual partners": Number(partners),
        "Smokes": Number(smokes),
        "STDs": Number(stds),
        "Dx": Number(dx)
    })
  });

  const data = await response.json();

  const probText =
    typeof data.probability === "number"
      ? ` (p=${data.probability.toFixed(3)}, threshold=${data.threshold ?? 0.5})`
      : "";

  document.getElementById("result").innerText =
    data.prediction === 1
      ? `⚠️ High Risk of Cervical Cancer${probText}`
      : `✅ Low Risk of Cervical Cancer${probText}`;
  }

  catch (error) {
    console.error(error);
    alert("Unable to connect to backend");
  }
 
}

