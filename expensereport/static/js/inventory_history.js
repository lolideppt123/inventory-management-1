const outputTable = document.querySelector(".output-table");
const outputTableBody = document.querySelector(".output-table-body");
const result = document.querySelector(".no-result-display");
const product_name = document.querySelector("#product_name");

const appTable = document.querySelector(".app-table");

const pagination = document.querySelector(".pagination-container");


outputTable.style.display = "none";
// result.style.display = "none";

window.addEventListener("load", init, false);
product_name.addEventListener("change", init, false);

function init() {
    product = product_name.value.trim();
    outputTableBody.innerHTML = "";
    fetch("", {
        body: JSON.stringify({ fieldValue: product }),
        method: "POST",
    })
        .then(response => {
            res = response.json();
            console.log(res);
            return res;
        })
        .then(response => {
            appTable.style.display = 'none';
            outputTable.style.display = 'block';
            console.log(response);

            if (response.length === 0) {
                outputTable.style.display = "none";
                result.style.display = "block";
                console.log('response = 0');
            }
            else {
                result.style.display = "none";

                console.log("imherer");
                response.forEach(item => {
                    if (item.transaction_type === "Sales") {
                        outputTableBody.innerHTML += `
                        <tr>
                        <td>${item.date}</td>
                        <td>${item.customer_supplier}</td>
                        <td>${item.product_name}</td>
                        <td>(${item.quantity})</td>
                        <td>${item.transaction_type}</td>
                        <td>${item.current_inventory}</td>
                        </tr>
                        `;
                    }
                    else if (item.transaction_type === "Inventory") {
                        outputTableBody.innerHTML += `
                        <tr>
                        <td>${item.date}</td>
                        <td>SUPPLIER</td>
                        <td>${item.product_name}</td>
                        <td>${item.quantity}</td>
                        <td>${item.product_unit}</td>
                        <td>${item.current_inventory}</td>
                        </tr>
                        `;
                    }
                }
                );

            }

        })

}