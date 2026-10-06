
function createTaskChart(completedTasks, pendingTasks) {

    const canvas = document.getElementById("taskChart");

    if (!canvas) {
        return;
    }

    new Chart(canvas, {

        type: "doughnut",

        data: {

            labels: [
                "Completed",
                "Pending"
            ],

            datasets: [
                {
                    data: [
                        completedTasks,
                        pendingTasks
                    ]
                }
            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "bottom"
                },

                title: {
                    display: false
                }

            }

        }

    });
}

