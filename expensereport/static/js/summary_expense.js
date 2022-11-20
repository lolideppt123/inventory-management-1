const renderChart = (labels, data) => {
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: labels,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Expense per Category'
                },
                subtitle: {
                    display: true,
                    text: 'Last 6-month Expenses'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

// const getChartData = () => {
//     console.log("fetching");
//     fetch('expense-category-summary')
//         .then((res) => {
//             console.log(res)
//             return res.json()
//         })
//         .then((result) => {
//             console.log("results", result);

//             renderChart([], []);
//         });
// }

async function getChartData() {
    const response = await fetch("expense-category-summary");
    console.log(response);
    const processResponse = await response.json();
    const category_data = processResponse.expense_category_data;
    console.log(processResponse);
    console.log(Object.keys(category_data));

    const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
    renderChart(labels, data);
}

document.onload = getChartData();




