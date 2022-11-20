const searchField = document.querySelector("#searchText");
const appTable = document.querySelector(".app-table");
const outputTable = document.querySelector(".output-table");
const outputTableBody = document.querySelector(".output-table-body");
const pagination = document.querySelector(".pagination-container");
const result = document.querySelector(".no-result-display");

outputTable.style.display = "none";
result.style.display = "none";

searchField.addEventListener("keyup", e => {
    console.log(777, 777);
    const searchValue = e.target.value;
    pagination.style.display = "none";

    // Adds invalid styles when user type in invalid info.
    if (searchValue.trim().length > 0) {
        outputTableBody.innerHTML = "";
        fetch("search-income", {
            body: JSON.stringify({ fieldValue: searchValue }),
            method: "POST",
        })
            .then(response => {
                res = response.json();
                console.log(res);
                return res; //can only consume Response.json() once.
            })
            .then(response => {
                // console.log("data", response);
                console.log("data", response);
                appTable.style.display = 'none';
                outputTable.style.display = 'block';

                if (response.length === 0) {
                    outputTable.style.display = "none";
                    result.style.display = "block";
                }
                else {
                    result.style.display = "none";
                    response.forEach(item => {
                        outputTableBody.innerHTML += `
                            <tr>
                            <td>${item.amount}</td>
                            <td>${item.source}</td>
                            <td>${item.description}</td>
                            <td>${item.date}</td>
                            </tr>
                        `;
                    });


                }

            })
    }
    else {
        outputTable.style.display = 'none';
        appTable.style.display = 'block';
        pagination.style.display = 'block';

    }
});